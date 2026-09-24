# -*- coding: utf-8 -*-
"""Gerador de paginas de SEO programatico do Album Coletivo. Template + dados -> HTML estatico.
Rodar de dentro de apps/album:  python tools/gen_seo.py .
Cada pagina tem conteudo UNICO (anti-doorway): lead/why/guia/lista/FAQ proprios."""
import os, html, json, sys

REPO = sys.argv[1] if len(sys.argv) > 1 else "."
BASE = "https://giogas-pm.github.io/album"
OUT_DIR = os.path.join(REPO, "album-de-fotos")

def e(s): return html.escape(s, quote=True)

FAQ_COMUM = [
    ("Quanto custa?",
     "Criar o álbum e receber quantas fotos os convidados quiserem é de graça. Você só paga uma vez (R$39), se quiser, para baixar todas as fotos originais em alta resolução, deixar o álbum permanente e tirar a marca. Não tem assinatura."),
    ("Os convidados precisam instalar app ou criar conta?",
     "Não. Cada convidado só abre o link (ou escaneia o QR) no navegador do celular e manda as fotos. Sem download, sem cadastro."),
    ("Funciona com a internet ruim do salão?",
     "Sim — foi feito pra isso. A foto é comprimida no próprio celular e entra numa fila que sobe sozinha quando a conexão firma. O convidado pode até fechar a página que a foto não se perde."),
]

def cta_href(): return "/album/?src=seo"

PAGES = [
{
 "slug":"album-colaborativo-casamento","kw":"álbum de fotos colaborativo para casamento",
 "title":"Álbum de Fotos Colaborativo para Casamento — Junte as Fotos dos Convidados | Álbum Coletivo",
 "h1":"Álbum de fotos colaborativo para o seu casamento",
 "desc":"Junte num só lugar as fotos que todos os convidados tiraram no seu casamento. Cada um manda pelo link ou QR na mesa — sem app, sem conta. Baixe tudo em alta.",
 "lead":"O fotógrafo entrega as fotos oficiais semanas depois — mas as melhores lembranças muitas vezes estão nos celulares dos convidados: aquele momento espontâneo na pista, o abraço da avó, a mesa rindo. O problema é que essas fotos ficam espalhadas em dezenas de celulares e somem no grupo do WhatsApp, comprimidas e sem organização. Um álbum colaborativo resolve: todo mundo joga as fotos num lugar só, e você fica com o casamento inteiro visto por todos os olhares.",
 "why":"Reunir as fotos dos convidados é o jeito mais barato de multiplicar as memórias do casamento: são centenas de cliques que o fotógrafo não pegou, de graça. Com um álbum coletivo, você manda um link (ou põe um QR na mesa), cada convidado envia em segundos e você baixa tudo em alta no final. Nada de pedir foto de um em um no WhatsApp depois.",
 "guide":[
   "Crie o álbum antes do casamento e gere o QR — dá pra imprimir num plaquinha bonita pra cada mesa.",
   "Peça ao mestre de cerimônias ou DJ pra avisar: \"mandem as fotos no QR da mesa\".",
   "Deixe o álbum aberto por alguns dias depois da festa — muita gente só manda as fotos no dia seguinte.",
 ],
 "list_title":"Onde espalhar o link/QR do álbum no casamento",
 "list_intro":"Quanto mais visível, mais fotos você recebe:",
 "list_items":[
   "Um QR impresso em cada mesa dos convidados (o jeito que mais funciona).",
   "No convite digital e no grupo de WhatsApp dos padrinhos e família.",
   "Numa placa na entrada da festa, junto do mapa de mesas.",
   "No telão, entre uma música e outra, com o QR grande.",
   "Nas lembrancinhas — um cartãozinho com o QR e \"mande suas fotos aqui\".",
 ],
 "faq":[
   ("As fotos vêm em boa qualidade pra imprimir depois?","Sim. O convidado envia a foto original do celular e você baixa em alta resolução — dá pra imprimir e montar um álbum físico do casamento com as fotos de todo mundo."),
 ],
},
{
 "slug":"qr-code-fotos-convidados","kw":"qr code para convidados enviarem fotos",
 "title":"QR Code para Convidados Enviarem Fotos da Festa | Álbum Coletivo",
 "h1":"QR code na mesa: os convidados enviam as fotos na hora",
 "desc":"Crie um QR code para os convidados enviarem as fotos da festa direto do celular. Coloque na mesa, todo mundo escaneia e manda — sem app e sem cadastro.",
 "lead":"Um QR code na mesa da festa é a forma mais simples de juntar as fotos de todo mundo: o convidado aponta a câmera, abre o link e manda as fotos que acabou de tirar. Sem pedir, sem coletar depois, sem grupo de WhatsApp virando bagunça. A festa acontece e as fotos vão caindo no álbum sozinhas.",
 "why":"O QR transforma o momento offline (a festa) em online (o álbum) sem atrito. Diferente de pedir \"manda depois no meu WhatsApp\" — que quase ninguém faz —, o QR na mesa capta a foto no calor do momento, quando o convidado ainda está com o celular na mão. E como funciona no navegador, ninguém precisa instalar nada.",
 "guide":[
   "Gere o QR do álbum e imprima grande o suficiente pra escanear de longe na mesa.",
   "Escreva uma chamada clara embaixo: \"Tirou foto? Manda aqui 📸\".",
   "Teste o QR com o seu próprio celular antes de imprimir em quantidade.",
 ],
 "list_title":"Dicas pra o QR funcionar bem na festa",
 "list_intro":"Pra não ter convidado travando na hora:",
 "list_items":[
   "QR com pelo menos 5 cm de lado — celular escaneia mais fácil.",
   "Bom contraste (QR escuro em fundo claro) e sem brilho/plástico refletindo.",
   "Uma frase curta explicando o que é: \"álbum de fotos da festa\".",
   "Coloque também o link escrito, pra quem tiver dificuldade com o QR.",
   "Reforce no telão ou no microfone pelo menos uma vez durante a festa.",
 ],
 "faq":[
   ("Preciso de algum aparelho ou impressora especial?","Não. Você gera o QR no site, baixa a imagem e imprime numa impressora comum (ou manda pra gráfica junto com a decoração). Os convidados usam a câmera normal do celular."),
 ],
},
{
 "slug":"como-juntar-fotos-dos-convidados","kw":"como juntar as fotos dos convidados",
 "title":"Como Juntar as Fotos dos Convidados da Festa num Lugar Só | Álbum Coletivo",
 "h1":"Como juntar as fotos dos convidados num lugar só",
 "desc":"Cansou de pedir foto no WhatsApp? Veja como juntar as fotos de todos os convidados da festa num álbum só, em alta qualidade, sem app e sem cadastro.",
 "lead":"Depois da festa vem a peregrinação: pedir as fotos no grupo, um manda, outro esquece, as que chegam vêm espremidas e sem qualidade pelo WhatsApp. No fim você junta um punhado de fotos ruins e perde as melhores. Dá pra fazer diferente: um álbum coletivo em que cada convidado joga as fotos direto, em alta, de forma organizada.",
 "why":"Centralizar as fotos num álbum resolve os três problemas de sempre: some (fica tudo salvo num lugar), perde qualidade (as fotos vão em alta, não comprimidas pelo WhatsApp) e dá trabalho (ninguém precisa coletar de um em um). Você manda um link uma vez e as fotos aparecem sozinhas.",
 "guide":[
   "Crie o álbum e compartilhe o link no grupo da festa — de preferência já durante o evento.",
   "Se for festa presencial, use também um QR na mesa pra captar no momento.",
   "Reforce o pedido no dia seguinte: \"quem tirou foto, manda no álbum\" com o link.",
 ],
 "list_title":"Por que o WhatsApp é ruim pra juntar fotos",
 "list_intro":"E como o álbum coletivo resolve cada ponto:",
 "list_items":[
   "O WhatsApp comprime a foto e ela perde qualidade — no álbum, vai a original em alta.",
   "As fotos se misturam com mensagens e somem no histórico — no álbum, ficam todas juntas.",
   "Você depende de cada um se lembrar de mandar — o QR na festa capta na hora.",
   "Baixar tudo do grupo é um inferno — no álbum, você baixa o pacote inteiro de uma vez.",
   "Vídeos e áudios entopem o grupo — o álbum é só pra as fotos da festa.",
 ],
 "faq":[
   ("E quem não estava na festa, consegue ver as fotos?","Sim, qualquer pessoa com o link vê a galeria coletiva. Só o organizador (você) pode baixar tudo em alta e apagar alguma foto, se precisar."),
 ],
},
{
 "slug":"site-para-convidados-enviarem-fotos","kw":"site para convidados enviarem fotos",
 "title":"Site para os Convidados Enviarem Fotos da Festa (Grátis) | Álbum Coletivo",
 "h1":"Um site para os convidados enviarem as fotos",
 "desc":"Um site simples para os convidados enviarem as fotos da festa: eles abrem o link, escolhem as fotos e pronto. Sem instalar app, sem criar conta. Grátis pra começar.",
 "lead":"Você não precisa de um aplicativo complicado nem pedir pra ninguém baixar nada. Um site onde o convidado abre o link, seleciona as fotos e envia já resolve — e funciona no celular de todo mundo, iPhone ou Android. A ideia é tirar todo atrito: quanto mais fácil, mais fotos você recebe.",
 "why":"Pedir pra instalar um app afasta metade dos convidados — principalmente os mais velhos, que são justamente quem tira as fotos mais especiais. Um site que abre no navegador, sem cadastro, faz todo mundo participar. E como as fotos sobem numa fila resiliente, nem a internet ruim da festa atrapalha.",
 "guide":[
   "Compartilhe o link do álbum no grupo e/ou como QR na festa.",
   "Deixe claro que é só abrir e mandar — sem baixar app, sem login.",
   "Mantenha o álbum aberto alguns dias pra recolher as fotos que chegam depois.",
 ],
 "list_title":"O que faz um bom site de fotos coletivas",
 "list_intro":"O que realmente importa na hora de escolher:",
 "list_items":[
   "Funcionar sem app e sem cadastro — atrito zero pro convidado.",
   "Aguentar internet ruim: a foto entra numa fila e sobe sozinha.",
   "Guardar a foto original em alta, não uma versão comprimida.",
   "Ter QR pronto pra imprimir e espalhar na festa.",
   "Deixar você baixar tudo de uma vez no final.",
 ],
 "faq":[
   ("Funciona no iPhone e no Android?","Nos dois. Como é um site que roda no navegador, qualquer celular consegue enviar as fotos — não importa a marca nem o modelo."),
 ],
},
{
 "slug":"album-de-fotos-aniversario","kw":"álbum de fotos coletivo de aniversário",
 "title":"Álbum de Fotos Coletivo de Aniversário — Junte as Fotos da Festa | Álbum Coletivo",
 "h1":"Álbum de fotos coletivo para o aniversário",
 "desc":"Junte as fotos que todos tiraram no aniversário num álbum só. Convidados mandam pelo link ou QR, sem app. Baixe tudo em alta e guarde a festa inteira.",
 "lead":"Aniversário é aquela festa em que todo mundo fotografa: a hora do parabéns, a criançada correndo, os amigos reunidos. Mas cada foto fica num celular diferente e você só vê um pedacinho. Um álbum coletivo junta tudo — de todos os convidados — pra você reviver a festa inteira e guardar de lembrança.",
 "why":"Num aniversário, as melhores fotos costumam ser as espontâneas que os convidados tiram, não as posadas. Reunir tudo num álbum garante que nenhuma se perca e que você tenha a festa vista por vários ângulos. Vale pra aniversário infantil, de 15 anos, de adulto ou aquela surpresa.",
 "guide":[
   "Crie o álbum e mande o link no grupo dos convidados antes da festa.",
   "Na festa, deixe um QR visível (na mesa do bolo é ótimo) pra galera mandar na hora.",
   "Depois, poste o link nas fotos que você mesmo publicar: \"tem mais no álbum\".",
 ],
 "list_title":"Momentos do aniversário que valem estar no álbum",
 "list_intro":"Peça pros convidados não deixarem faltar:",
 "list_items":[
   "A hora do parabéns e o sopro das velinhas.",
   "A reação de quem chegou de surpresa.",
   "A galera na pista ou brincando.",
   "As fotos em grupo e os detalhes da decoração.",
   "Os bastidores engraçados que só quem estava perto pegou.",
 ],
 "faq":[
   ("Serve pra aniversário infantil também?","Serve. Os pais dos coleguinhas mandam as fotos das crianças pelo link, e você junta tudo sem sair pedindo foto no grupo da escola depois."),
 ],
},
{
 "slug":"compartilhar-fotos-da-festa","kw":"como compartilhar as fotos da festa",
 "title":"Como Compartilhar as Fotos da Festa com Todos os Convidados | Álbum Coletivo",
 "h1":"Como compartilhar as fotos da festa com todo mundo",
 "desc":"A melhor forma de compartilhar as fotos da festa: um álbum coletivo onde todos veem e mandam fotos pelo link. Sem app, em alta qualidade. Grátis pra começar.",
 "lead":"Terminou a festa e todo mundo quer ver as fotos. Mandar uma por uma no WhatsApp é inviável, e o grupo vira uma bagunça comprimida. Compartilhar um álbum único — onde todos veem a galeria e ainda podem somar as próprias fotos — é muito mais prático e bonito.",
 "why":"Um álbum coletivo é ao mesmo tempo o lugar de guardar e o de compartilhar: você manda um único link e todo mundo acessa a festa inteira, em boa qualidade. E como cada convidado também pode enviar, o álbum só cresce — vira a memória oficial da festa, feita por todos.",
 "guide":[
   "Compartilhe um único link do álbum com todos os convidados.",
   "Incentive quem acessa a também mandar as próprias fotos — o álbum fica mais completo.",
   "Fixe o link no grupo pra quem chegar depois achar fácil.",
 ],
 "list_title":"Formas de compartilhar o álbum",
 "list_intro":"Escolha as que combinam com a sua festa:",
 "list_items":[
   "Link no grupo de WhatsApp da festa (o mais direto).",
   "QR impresso na mesa, pra quem ainda está no evento.",
   "Story ou post nas redes com o link na legenda.",
   "No convite digital, já convidando a mandar fotos.",
   "Por mensagem individual pra quem você sabe que tirou muitas fotos.",
 ],
 "faq":[
   ("Todo mundo consegue ver e baixar as fotos?","Ver, sim: qualquer um com o link vê a galeria. O download de tudo em alta fica com o organizador, que paga uma vez pra liberar o pacote completo do álbum."),
 ],
},
{
 "slug":"fotos-de-casamento-dos-convidados","kw":"reunir as fotos de casamento dos convidados",
 "title":"Como Reunir as Fotos de Casamento dos Convidados | Álbum Coletivo",
 "h1":"Reúna as fotos de casamento que os convidados tiraram",
 "desc":"As fotos dos convidados são metade das memórias do casamento. Veja como reuni-las num álbum só, em alta, sem depender do grupo do WhatsApp. Grátis pra começar.",
 "lead":"O casal recebe as fotos do fotógrafo, mas os convidados vão embora com centenas de cliques no celular — e quase todos se perdem. Aquele momento em que a tia chorou, o brinde dos amigos, a saída dos noivos vista da pista. Reunir essas fotos num álbum é resgatar metade das memórias do casamento que, do contrário, sumiriam.",
 "why":"As fotos dos convidados têm um valor que a foto oficial não tem: são os olhares de quem ama os noivos, os momentos que o fotógrafo não estava por perto. Juntá-las num álbum coletivo, em alta, é dar aos noivos um segundo casamento em imagens — e sai de graça, porque quem fotografou foram os próprios convidados.",
 "guide":[
   "Monte o álbum antes do casamento e deixe o QR pronto pra imprimir nas mesas.",
   "Combine com os padrinhos de espalharem o link no dia.",
   "Depois da lua de mel, reative o pedido: muita gente ainda tem fotos pra mandar.",
 ],
 "list_title":"Fotos de casamento que só os convidados têm",
 "list_intro":"As que raramente aparecem no álbum oficial:",
 "list_items":[
   "A reação da família durante a cerimônia, vista da plateia.",
   "Os bastidores da pista de dança já no fim da festa.",
   "As mesas rindo e os reencontros entre convidados.",
   "Os detalhes que cada um reparou — flores, doces, lembrancinhas.",
   "Os vídeos e cliques espontâneos da saída dos noivos.",
 ],
 "faq":[
   ("Dá pra usar as fotos dos convidados num álbum impresso?","Dá. Como você baixa as fotos originais em alta, é possível selecionar as melhores e montar um álbum físico ou fotolivro do casamento com o olhar dos convidados."),
 ],
},
{
 "slug":"app-para-juntar-fotos-festa","kw":"app para juntar fotos da festa",
 "title":"App para Juntar as Fotos da Festa? Use um Álbum sem Instalar Nada | Álbum Coletivo",
 "h1":"Precisa de um app pra juntar as fotos da festa?",
 "desc":"Você não precisa que os convidados instalem um app pra juntar as fotos da festa. Um álbum coletivo pelo link resolve — sem download, sem conta, em alta. Grátis.",
 "lead":"Procurando um \"app pra juntar as fotos da festa\"? A verdade é que pedir instalação de app é o maior inimigo da adesão: metade dos convidados não baixa. O que funciona é o oposto — um álbum que abre no navegador, sem instalar nada, onde cada um manda as fotos em segundos.",
 "why":"Sem app pra baixar, sem conta pra criar, a barreira cai a zero e muito mais gente participa. O álbum coletivo faz tudo o que você esperaria de um app — galeria, envio pelo celular, download em alta — mas roda direto no link, o que é decisivo pra captar as fotos dos convidados menos habituados a tecnologia.",
 "guide":[
   "Esqueça a instalação: compartilhe o link do álbum e/ou o QR.",
   "Explique que é só abrir e mandar — isso já aumenta muito a adesão.",
   "Use o QR na festa pra captar quem está com o celular na mão.",
 ],
 "list_title":"App instalável x álbum pelo link",
 "list_intro":"Por que o link ganha pra fotos de festa:",
 "list_items":[
   "Sem download: ninguém precisa liberar espaço nem instalar nada.",
   "Sem cadastro: nada de senha, e-mail ou verificação.",
   "Funciona em qualquer celular, novo ou antigo.",
   "Você adiciona à tela inicial se quiser (é um PWA), mas não é obrigatório.",
   "Mesmo com internet ruim, a foto entra na fila e sobe sozinha.",
 ],
 "faq":[
   ("Então não é um aplicativo de verdade?","É um app que roda no navegador (PWA): dá pra adicionar à tela do celular como um aplicativo, mas sem passar pela loja nem instalar. Pro convidado, é só abrir o link."),
 ],
},
]

CSS = """
:root{--bg:#f5f3fb;--bg2:#ece8fb;--ink:#2b2740;--muted:#7b7699;--accent:#6c5ce7;--accent2:#a66cff;--card:#fff;--line:#e6e1f5;--ok:#2e9e5b;--shadow:0 10px 30px rgba(80,64,150,.12)}
*{box-sizing:border-box}html,body{margin:0}
body{font-family:'Inter',system-ui,sans-serif;color:var(--ink);background:radial-gradient(1200px 600px at 80% -10%,var(--bg2),transparent),var(--bg);min-height:100vh;-webkit-font-smoothing:antialiased;line-height:1.6}
h1,h2,h3{font-family:'Fraunces',Georgia,serif;font-weight:600;line-height:1.15}
a{color:var(--accent);text-decoration:none}a:hover{text-decoration:underline}
.wrap{max-width:860px;margin:0 auto;padding:0 20px}
nav{display:flex;align-items:center;justify-content:space-between;padding:20px 0}
.brand{display:flex;align-items:center;gap:10px;font-family:'Fraunces';font-weight:700;font-size:22px;color:var(--ink)}
.logo{width:34px;height:34px;border-radius:10px;background:linear-gradient(135deg,var(--accent),var(--accent2));display:grid;place-items:center;color:#fff;font-size:18px}
.btn{display:inline-block;border:none;border-radius:999px;padding:14px 24px;font-weight:600;font-size:16px;cursor:pointer;font-family:inherit;background:linear-gradient(135deg,var(--accent),var(--accent2));color:#fff;box-shadow:0 8px 20px rgba(108,92,231,.35)}
.btn:hover{text-decoration:none;box-shadow:0 12px 26px rgba(108,92,231,.45)}
.hero{text-align:center;padding:26px 0 8px}
.hero h1{font-size:clamp(30px,5vw,46px);margin:0 0 16px}
.lead{font-size:18px;color:var(--muted);max-width:660px;margin:0 auto 22px}
.card{background:var(--card);border:1px solid var(--line);border-radius:20px;box-shadow:var(--shadow);padding:26px;margin:22px 0}
h2{font-size:26px;margin:34px 0 12px}
.steps{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:14px 0}
.step{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:18px;box-shadow:var(--shadow)}
.step .n{width:30px;height:30px;border-radius:9px;background:var(--bg2);display:grid;place-items:center;font-weight:700;margin-bottom:8px;font-family:'Fraunces'}
.step h3{margin:0 0 6px;font-size:17px}.step p{margin:0;color:var(--muted);font-size:14px}
ul.items{list-style:none;padding:0;margin:0;display:grid;gap:10px}
ul.items li{background:#fffdfb;border:1px solid var(--line);border-left:4px solid var(--accent2);border-radius:10px;padding:12px 14px;font-size:15.5px}
.faq dt{font-weight:600;margin-top:16px}.faq dd{margin:6px 0 0;color:var(--muted)}
.related{display:flex;flex-wrap:wrap;gap:10px;margin-top:12px}
.related a{background:var(--card);border:1px solid var(--line);border-radius:999px;padding:8px 15px;font-size:14px;box-shadow:var(--shadow);color:var(--ink)}
.related a:hover{text-decoration:none;border-color:var(--accent)}
.center{text-align:center}
footer{text-align:center;color:var(--muted);font-size:13px;padding:34px 0 44px}
@media(max-width:720px){.steps{grid-template-columns:1fr}}
"""

HEAD = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>{title}</title>
<meta name="description" content="{desc}"/>
<link rel="canonical" href="{canon}"/>
<meta property="og:type" content="website"/>
<meta property="og:title" content="{title}"/>
<meta property="og:description" content="{desc}"/>
<meta property="og:url" content="{canon}"/>
<meta property="og:site_name" content="Álbum Coletivo"/>
<meta name="robots" content="index,follow"/>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet"/>
<style>{css}</style>
{jsonld}
</head>
<body>
<div class="wrap">
<nav><a class="brand" href="/album/"><span class="logo">📸</span> Álbum Coletivo</a><a class="btn" style="padding:10px 18px;font-size:14px" href="{cta}">Criar álbum grátis</a></nav>
"""

FOOT = """<footer>Álbum Coletivo — junte as fotos da festa num álbum só · <a href="/album/">criar meu álbum grátis</a></footer>
</div>
<script>
(function(){try{
  var q=new URLSearchParams(location.search), src=q.get('src')||'seo';
  document.querySelectorAll('a[href*="/album/?"]').forEach(function(a){
    try{var u=new URL(a.getAttribute('href'), location.origin); u.searchParams.set('src',src); a.setAttribute('href', u.pathname+u.search);}catch(e){}
  });
  var SB="https://diemqzngskmcuytkzjhr.supabase.co";
  var K="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRpZW1xem5nc2ttY3V5dGt6amhyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODI4NDM0MDEsImV4cCI6MjA5ODQxOTQwMX0.w5-w8bU6qFQqIFBDOiNsUvOWbXqeOZSH6tveyLdADx0";
  fetch(SB+"/rest/v1/album_eventos",{method:"POST",headers:{apikey:K,Authorization:"Bearer "+K,"Content-Type":"application/json"},body:JSON.stringify({evento:"seo_land",slug:location.pathname,meta:{src:src}})}).catch(function(){});
}catch(e){}})();
</script>
</body>
</html>"""

def _script(obj): return '<script type="application/ld+json">'+json.dumps(obj,ensure_ascii=False)+'</script>'

def jsonld_page(faqs, canon, name):
    faq={"@context":"https://schema.org","@type":"FAQPage",
         "mainEntity":[{"@type":"Question","name":q,
             "acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs]}
    howto={"@context":"https://schema.org","@type":"HowTo",
        "name":"Como juntar as fotos dos convidados num álbum coletivo",
        "step":[
          {"@type":"HowToStep","position":1,"name":"Crie o álbum","text":"Diga o nome da festa. Leva menos de 1 minuto e é grátis."},
          {"@type":"HowToStep","position":2,"name":"Espalhe o link ou QR","text":"Cada convidado abre no navegador e envia as fotos — sem app e sem cadastro."},
          {"@type":"HowToStep","position":3,"name":"Baixe tudo em alta","text":"No final, baixe todas as fotos originais em alta resolução num pacote só."},
        ]}
    crumb={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Álbum Coletivo","item":BASE+"/"},
        {"@type":"ListItem","position":2,"name":"Álbum de fotos","item":BASE+"/album-de-fotos/"},
        {"@type":"ListItem","position":3,"name":name,"item":canon},
    ]}
    return "\n".join(_script(o) for o in (howto,faq,crumb))

def steps_html():
    return ('<div class="steps">'
      '<div class="step"><div class="n">1</div><h3>Crie o álbum</h3><p>Diga o nome da festa. Leva menos de 1 minuto e é grátis.</p></div>'
      '<div class="step"><div class="n">2</div><h3>Espalhe o link ou QR</h3><p>Cada convidado abre no navegador e manda as fotos — sem app, sem conta.</p></div>'
      '<div class="step"><div class="n">3</div><h3>Baixe tudo em alta</h3><p>No final, baixe todas as fotos originais num pacote só.</p></div>'
      '</div>')

def related_html(cur_slug):
    links=[]
    for p in PAGES:
        if p["slug"]==cur_slug: continue
        links.append('<a href="/album/album-de-fotos/%s/">%s</a>'%(p["slug"], e(p["kw"].capitalize())))
    return '<div class="related">'+''.join(links)+'</div>'

def build_page(p):
    canon = "%s/album-de-fotos/%s/"%(BASE,p["slug"])
    cta = cta_href()
    faqs = p["faq"] + FAQ_COMUM
    jsonld = jsonld_page(faqs, canon, p["h1"])
    head = HEAD.format(title=e(p["title"]),desc=e(p["desc"]),canon=canon,css=CSS,jsonld=jsonld,cta=e(cta))
    out=[head]
    out.append('<section class="hero"><h1>%s</h1><p class="lead">%s</p><a class="btn" href="%s">Criar álbum da festa grátis</a></section>'
               %(e(p["h1"]),e(p["lead"]),e(cta)))
    out.append('<h2>Como funciona</h2>'+steps_html())
    out.append('<div class="card"><h2 style="margin-top:0">Por que vale a pena</h2><p>%s</p></div>'%e(p["why"]))
    if p.get("guide"):
        out.append('<h2>Como organizar</h2>')
        out.append('<ul class="items">'+''.join('<li>%s</li>'%e(g) for g in p["guide"])+'</ul>')
    out.append('<h2>%s</h2>'%e(p["list_title"]))
    if p.get("list_intro"):
        out.append('<p style="color:var(--muted)">%s</p>'%e(p["list_intro"]))
    out.append('<ul class="items">'+''.join('<li>%s</li>'%e(x) for x in p["list_items"])+'</ul>')
    out.append('<h2>Perguntas frequentes</h2><dl class="faq">'+''.join('<dt>%s</dt><dd>%s</dd>'%(e(q),e(a)) for q,a in faqs)+'</dl>')
    out.append('<div class="card center"><h2 style="margin-top:0">Pronto pra começar?</h2><p style="color:var(--muted)">Crie o álbum da sua festa agora. Grátis pra receber as fotos dos convidados — você só paga se quiser baixar tudo em alta.</p><a class="btn" href="%s">Criar meu álbum grátis 📸</a></div>'%e(cta))
    out.append('<h2>Veja também</h2>'+related_html(p["slug"]))
    out.append(FOOT)
    return "\n".join(out)

def build_hub():
    canon = "%s/album-de-fotos/"%BASE
    cta = cta_href()
    title="Álbum de Fotos Colaborativo: Junte as Fotos dos Convidados (Grátis) | Álbum Coletivo"
    desc="Junte as fotos de todos os convidados da festa num álbum só. Cada um manda pelo link ou QR, sem app e sem conta. Baixe tudo em alta. Grátis pra começar."
    web={"@context":"https://schema.org","@type":"WebPage","name":title,"url":canon}
    jsonld=_script(web)
    head = HEAD.format(title=e(title),desc=e(desc),canon=canon,css=CSS,jsonld=jsonld,cta=e(cta))
    out=[head]
    out.append('<section class="hero"><h1>Álbum de fotos colaborativo: junte as fotos da festa</h1><p class="lead">Cada convidado manda as fotos que tirou pra um álbum só — pelo link ou por um QR na mesa. Sem app, sem cadastro, e você baixa tudo em alta no final. Aqui você encontra guias pra casamento, aniversário e qualquer festa.</p><a class="btn" href="%s">Criar meu álbum grátis</a></section>'%e(cta))
    out.append('<h2>Como funciona</h2>'+steps_html())
    out.append('<h2>Guias pra juntar as fotos da sua festa</h2><div class="related">')
    for p in PAGES:
        out.append('<a href="/album/album-de-fotos/%s/">%s</a>'%(p["slug"],e(p["kw"].capitalize())))
    out.append('</div>')
    out.append('<div class="card"><h2 style="margin-top:0">O que é o Álbum Coletivo</h2><p>O Álbum Coletivo é uma ferramenta gratuita pra criar um <strong>álbum de fotos colaborativo de festa</strong>: os convidados enviam as fotos que tiraram a partir de um único link (ou de um QR na mesa), sem instalar app e sem criar conta, e tudo aparece numa galeria coletiva. Foi feito pra funcionar mesmo com a <strong>internet ruim</strong> de salão: a foto é comprimida no celular e entra numa fila que sobe sozinha quando a conexão firma. Receber as fotos é grátis; você só paga uma vez, se quiser, pra baixar todas as originais em alta resolução e manter o álbum permanente.</p></div>')
    out.append(FOOT)
    return "\n".join(out)

def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path,"w",encoding="utf-8",newline="\n") as f:
        f.write(content)
    print("escrito:", path, "(%d bytes, ~%d palavras)"%(len(content.encode('utf-8')), len(content.split())))

write(os.path.join(OUT_DIR,"index.html"), build_hub())
for p in PAGES:
    write(os.path.join(OUT_DIR,p["slug"],"index.html"), build_page(p))

urls=[BASE+"/", BASE+"/album-de-fotos/"] + [BASE+"/album-de-fotos/%s/"%p["slug"] for p in PAGES]
sm=['<?xml version="1.0" encoding="UTF-8"?>','<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for u in urls:
    pr = "1.0" if u==BASE+"/" else ("0.9" if u.endswith("album-de-fotos/") else "0.8")
    sm.append("  <url><loc>%s</loc><changefreq>weekly</changefreq><priority>%s</priority></url>"%(u,pr))
sm.append("</urlset>")
write(os.path.join(REPO,"sitemap.xml"), "\n".join(sm))

robots="User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n"%BASE
write(os.path.join(REPO,"robots.txt"), robots)

print("\nTOTAL:", 1+len(PAGES), "paginas de conteudo + sitemap + robots")
