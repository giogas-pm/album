/* album-queue.js — motor de fila de upload resiliente.
   Roda IGUAL na página (window) e no Service Worker (importScripts).
   Garantia central: a foto NUNCA sai do IndexedDB local até ter
   confirmação dupla no servidor (arquivo no Storage + linha no banco).
   Tudo idempotente (UUID do cliente + upsert), então retry nunca duplica. */
(function (scope) {
  'use strict';

  var SB_URL = "https://diemqzngskmcuytkzjhr.supabase.co";
  var SB_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRpZW1xem5nc2ttY3V5dGt6amhyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODI4NDM0MDEsImV4cCI6MjA5ODQxOTQwMX0.w5-w8bU6qFQqIFBDOiNsUvOWbXqeOZSH6tveyLdADx0";
  var BUCKET = "album-fotos";
  var SB_H = { apikey: SB_KEY, Authorization: "Bearer " + SB_KEY };

  var DB_NAME = "album_q", DB_VER = 1, STORE = "photos";
  var MAX_BACKOFF = 60000; // teto de 60s entre tentativas

  /* ---------- IndexedDB ---------- */
  function openDB() {
    return new Promise(function (res, rej) {
      var rq = indexedDB.open(DB_NAME, DB_VER);
      rq.onupgradeneeded = function () {
        var db = rq.result;
        if (!db.objectStoreNames.contains(STORE)) {
          db.createObjectStore(STORE, { keyPath: "id" });
        }
      };
      rq.onsuccess = function () { res(rq.result); };
      rq.onerror = function () { rej(rq.error); };
    });
  }
  function tx(mode, fn) {
    return openDB().then(function (db) {
      return new Promise(function (res, rej) {
        var t = db.transaction(STORE, mode), st = t.objectStore(STORE), out;
        Promise.resolve(fn(st)).then(function (v) { out = v; });
        t.oncomplete = function () { res(out); };
        t.onerror = function () { rej(t.error); };
        t.onabort = function () { rej(t.error); };
      });
    });
  }
  function reqP(r) { return new Promise(function (res, rej) { r.onsuccess = function () { res(r.result); }; r.onerror = function () { rej(r.error); }; }); }

  function putRec(rec) { return tx("readwrite", function (st) { st.put(rec); }); }
  function delRec(id) { return tx("readwrite", function (st) { st.delete(id); }); }
  function getAll() { return tx("readonly", function (st) { return reqP(st.getAll()); }); }

  /* ---------- enfileirar (chamado pela página) ---------- */
  function enqueue(rec) {
    // rec: {id, slug, albumId, uploaderName, master(Blob), masterType, preview(Blob), w, h, bytes}
    rec.prevDone = false; rec.masterDone = false; rec.rowDone = false;
    rec.attempts = 0; rec.nextAt = 0; rec.lastError = null;
    rec.createdAt = Date.now();
    return putRec(rec);
  }

  /* modo avião simulado (teste/demo): quando ligado, todo upload falha
     de propósito, exercitando a fila + retry sem depender da rede real. */
  function offlineSim() { return !!scope.__albumOffline; }

  /* ---------- upload de um arquivo pro Storage (upsert = idempotente) ---------- */
  function uploadObject(path, blob, contentType) {
    if (offlineSim()) return Promise.reject(new Error("offline (simulado)"));
    return fetch(SB_URL + "/storage/v1/object/" + BUCKET + "/" + path, {
      method: "POST",
      headers: Object.assign({}, SB_H, { "Content-Type": contentType || "application/octet-stream", "x-upsert": "true" }),
      body: blob
    }).then(function (r) {
      if (r.ok) return true;
      return r.text().then(function (t) { throw new Error("storage " + r.status + " " + t.slice(0, 120)); });
    });
  }

  function insertRow(rec) {
    if (offlineSim()) return Promise.reject(new Error("offline (simulado)"));
    return fetch(SB_URL + "/rest/v1/album_fotos", {
      method: "POST",
      headers: Object.assign({}, SB_H, { "Content-Type": "application/json" }),
      body: JSON.stringify({
        id: rec.id, album_id: rec.albumId, uploader_name: rec.uploaderName || null,
        storage_path: rec.slug + "/" + rec.id,
        preview_path: rec.preview ? (rec.slug + "/" + rec.id + "_t.jpg") : null,
        width: rec.w || null, height: rec.h || null, bytes: rec.bytes || null
      })
    }).then(function (r) {
      if (r.status === 201 || r.status === 409) return true; // 409 = já inserido (retry) => sucesso
      return r.text().then(function (t) { throw new Error("row " + r.status + " " + t.slice(0, 120)); });
    });
  }

  /* ---------- avança UMA foto um passo de cada vez, persistindo ---------- */
  function advanceOne(rec) {
    var chain = Promise.resolve();
    if (!rec.prevDone) {
      chain = chain.then(function () {
        if (!rec.preview) { rec.prevDone = true; return; } // sem preview (ex.: HEIC) — master serve de fallback
        return uploadObject(rec.slug + "/" + rec.id + "_t.jpg", rec.preview, "image/jpeg").then(function () {
          rec.prevDone = true; return putRec(rec);
        });
      });
    }
    if (!rec.masterDone) {
      chain = chain.then(function () {
        return uploadObject(rec.slug + "/" + rec.id, rec.master, rec.masterType || "image/jpeg").then(function () {
          rec.masterDone = true; return putRec(rec);
        });
      });
    }
    if (!rec.rowDone) {
      chain = chain.then(function () {
        return insertRow(rec).then(function () { rec.rowDone = true; return putRec(rec); });
      });
    }
    return chain.then(function () {
      // confirmação dupla completa -> só agora libera o local
      return delRec(rec.id).then(function () { return "done"; });
    }).catch(function (err) {
      rec.attempts = (rec.attempts || 0) + 1;
      rec.lastError = String(err && err.message || err);
      var back = Math.min(MAX_BACKOFF, 1000 * Math.pow(2, rec.attempts)) * (0.7 + Math.random() * 0.6);
      rec.nextAt = Date.now() + back;
      return putRec(rec).then(function () { return "retry"; });
    });
  }

  /* ---------- pump: tenta avançar tudo que está elegível ---------- */
  var pumping = false;
  function pump() {
    if (pumping) return Promise.resolve({ skipped: true });
    pumping = true;
    var now = Date.now(), done = 0, retry = 0, pending = 0;
    return getAll().then(function (all) {
      var due = all.filter(function (r) { return (r.nextAt || 0) <= now; });
      pending = all.length;
      return due.reduce(function (p, rec) {
        return p.then(function () {
          return advanceOne(rec).then(function (res) {
            if (res === "done") { done++; pending--; } else { retry++; }
          });
        });
      }, Promise.resolve());
    }).then(function () {
      pumping = false;
      emit();
      return { done: done, retry: retry, pending: pending };
    }).catch(function (e) { pumping = false; return { error: String(e) }; });
  }

  function pendingCount() { return getAll().then(function (a) { return a.length; }); }
  function listPending() { return getAll(); }

  /* conexão voltou: zera o backoff pra TODAS as fotos tentarem já (não esperar 60s) */
  function retryNow() {
    return getAll().then(function (all) {
      return Promise.all(all.map(function (r) { r.nextAt = 0; return putRec(r); }));
    });
  }

  /* ---------- notificação simples de mudança de estado ---------- */
  function emit() {
    try {
      if (scope.document) { scope.dispatchEvent(new Event("album-queue-changed")); }
      else if (scope.clients && scope.clients.matchAll) {
        scope.clients.matchAll().then(function (cs) { cs.forEach(function (c) { c.postMessage({ type: "album-queue-changed" }); }); });
      }
    } catch (_) {}
  }

  scope.AlbumQueue = {
    enqueue: enqueue, pump: pump, pendingCount: pendingCount, listPending: listPending, retryNow: retryNow,
    SB_URL: SB_URL, SB_KEY: SB_KEY, SB_H: SB_H, BUCKET: BUCKET
  };
})(typeof self !== "undefined" ? self : this);
