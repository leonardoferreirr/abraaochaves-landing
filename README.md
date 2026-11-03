# Abraão Chaves | landing

Landing de Abraão Chaves (logoterapeuta, filósofo e escritor, @abraaochavess). Página estática, sem dependências.
Todos os botões levam ao WhatsApp +55 91 8063-2788 passando por `obrigado.html`, que registra o evento
`conversao_whatsapp` no dataLayer (com o contexto do botão) e abre a conversa com a mensagem certa
(atendimento, livro ou empresa).

## Como mexer
- Edite `src/index.html` e `src/obrigado.html`, depois rode `python3 build.py` (gera os arquivos da raiz).
- O logo vem do traço de `tools/logo-groups.json`; `python3 tools/logo.py` refaz `partials/logo-defs.html` e o `favicon.svg`.
- Movimento em `assets/main.js` (símbolo se desenhando no topo, frase acendendo, estrada dos passos, livro 3D, faixas).
- Conferir: `python3 tools/shots.py <pasta> 390 844` (fotos ao longo da página) e `python3 tools/serve.py` (servidor com gzip para o Lighthouse).

## Busca e IA (SEO, AEO e GEO)
- O `build.py` gera o `<head>` de busca do `index.html` (título, descrição, canonical, Open Graph e Twitter),
  o schema em JSON-LD (Person, ProfessionalService com os serviços, Book, WebSite e WebPage), o `robots.txt`,
  o `sitemap.xml` e o `llms.txt`.
- Título e descrição do Google ficam em `TITULO` e `DESCRICAO` no topo do `build.py`. O h1 da página não muda.
- Passos, situações, facetas, serviços para empresas e o texto do livro são lidos do próprio `src/index.html`:
  editou a página e rodou o build, o schema e o `llms.txt` acompanham.
- Não tem FAQPage porque a página não mostra perguntas e respostas. Se um FAQ visível entrar, ele pode ganhar o schema.
- O livro entra no schema sem capa (a da página é provisória), sem ISBN e sem data, que o site não informa.

## Como trocar de domínio sem perder SEO
1. Em `build.py`, troque `DOMINIO` pelo endereço novo (por exemplo `https://www.abraaochaves.com.br`, sem barra no fim).
2. Rode `python3 build.py`. Canonical, og:url, imagem de compartilhamento, schema, `sitemap.xml`, `robots.txt` e
   `llms.txt` passam a usar o domínio novo, e o `vercel.json` ganha o redirect permanente de `abraaochaves.vercel.app`
   para ele (308, que o Google trata como 301).
3. Adicione o domínio no projeto da Vercel (Settings, Domains) e aponte o DNS como a Vercel pedir.
4. Faça o push. Depois do deploy, confira que `https://abraaochaves.vercel.app/` responde com redirect para o domínio novo.
5. No Google Search Console, cadastre o domínio novo e envie o `sitemap.xml`.

## A preencher
- GTM: colar o container no `index.html` e no `obrigado.html`.
- Capa do livro *Entre o Céu e a Terra*: a da página é provisória, feita com o símbolo da marca. Trocar pela capa real.
- O botão "Conhecer o livro" do topo está oculto (`hidden`) a pedido; para voltar, é só tirar o atributo.
