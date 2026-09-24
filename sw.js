/* sw.js — offline shell + upload em background.
   Reusa o MESMO motor da página (album-queue.js), então a foto sobe
   mesmo com a aba fechada, quando a conexão voltar (Background Sync). */
importScripts("album-queue.js");

var CACHE = "album-shell-v2";
var SHELL = ["./", "./index.html", "./album-queue.js", "./manifest.json"];

self.addEventListener("install", function (e) {
  e.waitUntil(caches.open(CACHE).then(function (c) { return c.addAll(SHELL); }).then(function () { return self.skipWaiting(); }));
});

self.addEventListener("activate", function (e) {
  e.waitUntil(
    caches.keys().then(function (keys) {
      return Promise.all(keys.map(function (k) { return k === CACHE ? null : caches.delete(k); }));
    }).then(function () { return self.clients.claim(); })
  );
});

/* cache-first pro shell; rede pro resto (Supabase etc.) */
self.addEventListener("fetch", function (e) {
  var url = new URL(e.request.url);
  if (e.request.method !== "GET") return;
  if (url.origin === self.location.origin) {
    e.respondWith(
      caches.match(e.request).then(function (hit) {
        return hit || fetch(e.request).then(function (res) {
          var copy = res.clone();
          caches.open(CACHE).then(function (c) { try { c.put(e.request, copy); } catch (_) {} });
          return res;
        }).catch(function () { return caches.match("./index.html"); });
      })
    );
  }
});

/* Background Sync: drena a fila. Se sobrar pendência, rejeita pra
   o navegador reagendar automaticamente (com backoff próprio dele). */
self.addEventListener("sync", function (e) {
  if (e.tag === "album-drain") {
    e.waitUntil(
      self.AlbumQueue.pump().then(function () {
        return self.AlbumQueue.pendingCount();
      }).then(function (n) {
        if (n > 0) throw new Error("ainda ha " + n + " pendente(s) — reagendar");
      })
    );
  }
});

/* a página pode pedir um pump manual, ou espelhar o modo teste "internet ruim" */
self.addEventListener("message", function (e) {
  if (!e.data) return;
  if (e.data.type === "album-offline") { self.__albumOffline = !!e.data.on; }
  if (e.data.type === "album-pump") { e.waitUntil(self.AlbumQueue.pump()); }
});
