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

## A preencher
- `DOMINIO` em `build.py` quando houver endereço próprio (canonical e imagem de compartilhamento).
- GTM: colar o container no `index.html` e no `obrigado.html`.
- Capa do livro *Entre o Céu e a Terra*: a da página é provisória, feita com o símbolo da marca. Trocar pela capa real.
- O botão "Conhecer o livro" do topo está oculto (`hidden`) a pedido; para voltar, é só tirar o atributo.
