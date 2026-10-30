"""Monta index.html e obrigado.html a partir de src/.

Uso: python3 build.py   (roda tools/logo.py antes se o traço do logo mudar)
Troque DOMINIO quando o site tiver endereço próprio: entra no canonical e na imagem de compartilhamento.
"""
import os, random

DOMINIO = 'https://abraaochaves.vercel.app'  # trocar quando houver domínio próprio

AQUI = os.path.dirname(os.path.abspath(__file__))
WA = ('<svg viewBox="0 0 24 24" aria-hidden="true" fill="currentColor"><path d="M17.47 14.38c-.3-.15-1.76-.87-2.03-.97-.27-.1-.47-.15-.67.15-.2.3-.77.97-.94 1.16-.17.2-.35.22-.64.08-.3-.15-1.26-.47-2.39-1.48-.88-.79-1.48-1.76-1.65-2.06-.17-.3-.02-.46.13-.6.13-.14.3-.35.45-.52.15-.18.2-.3.3-.5.1-.2.05-.37-.03-.52-.07-.15-.67-1.61-.91-2.21-.25-.58-.49-.5-.67-.51h-.57c-.2 0-.52.08-.8.37-.27.3-1.04 1.02-1.04 2.48s1.07 2.88 1.21 3.07c.15.2 2.1 3.2 5.08 4.49.71.31 1.26.49 1.7.63.71.22 1.36.19 1.87.12.57-.09 1.76-.72 2-1.42.25-.69.25-1.29.18-1.41-.08-.13-.28-.2-.57-.35m-5.42 7.4h-.01a9.87 9.87 0 0 1-5.03-1.38l-.36-.21-3.74.98 1-3.65-.24-.37a9.86 9.86 0 0 1-1.51-5.26c0-5.45 4.44-9.88 9.89-9.88 2.64 0 5.12 1.03 6.99 2.9a9.83 9.83 0 0 1 2.89 6.99c0 5.45-4.44 9.88-9.88 9.88m8.41-18.3A11.82 11.82 0 0 0 12.05 0C5.5 0 .16 5.34.16 11.89c0 2.1.55 4.14 1.59 5.95L.06 24l6.3-1.65a11.88 11.88 0 0 0 5.69 1.45h.01c6.55 0 11.89-5.34 11.89-11.89 0-3.18-1.24-6.17-3.48-8.41z"/></svg>')
SETA = ('<svg class="seta" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.6" '
        'stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>')

defs = open(os.path.join(AQUI, 'partials', 'logo-defs.html')).read()

# folhas que caem no fundo: duas formas, desenhadas uma vez e reaproveitadas
FOLHA_DEFS = ('<svg class="defs" aria-hidden="true" focusable="false"><defs>'
              '<symbol id="folha-a" viewBox="0 0 40 64"><path d="M20 2C33 14 37 36 21 61C5 38 7 15 20 2Z"/>'
              '<path d="M20 7C21 25 21 43 21 58" fill="none" stroke="rgba(14,18,11,.28)" stroke-width="1.2"/></symbol>'
              '<symbol id="folha-b" viewBox="0 0 40 64"><path d="M20 5C35 11 38 32 22 51C6 32 6 13 20 5Z"/>'
              '<path d="M21 9C21 24 22 38 22 50L24 62" fill="none" stroke="rgba(14,18,11,.28)" stroke-width="1.2"/></symbol>'
              '</defs></svg>')

def folhas(semente, n, cores, opac):
    rnd = random.Random(semente)
    itens = []
    for k in range(n):
        x = (k + rnd.uniform(.1, .9)) / n * 100           # espalhadas pela largura, sem amontoar
        t = rnd.uniform(14, 24)
        itens.append(f'<span class="cai" style="--x:{x:.1f}%;--t:{t:.1f}s;--a:-{rnd.uniform(0, t):.1f}s;'
                     f'--e:{rnd.uniform(.6, 1.15):.2f};--c:{rnd.choice(cores)};--o:{rnd.uniform(*opac):.2f}">'
                     f'<span class="gira"><svg viewBox="0 0 40 64"><use href="#folha-{rnd.choice("ab")}"/></svg></span></span>')
    return '<div class="folhas" aria-hidden="true">' + ''.join(itens) + '</div>'

PARTES = {
    '<!--RAIZES_FRASE-->': open(os.path.join(AQUI, 'partials', 'raizes-frase.html')).read(),
    '<!--RAIZES_LIVRO-->': open(os.path.join(AQUI, 'partials', 'raizes-livro.html')).read(),
    '<!--FOLHAS_FRASE-->': folhas(3, 7, ['#798b4d', '#5e6e38', '#c9dca6'], (.22, .4)),
    '<!--FOLHAS_LIVRO-->': folhas(5, 12, ['#798b4d', '#5e6e38', '#9db070', '#c9dca6'], (.5, .85)),
}
canonical = f'<link rel="canonical" href="{DOMINIO}/">\n<meta property="og:url" content="{DOMINIO}/">' if DOMINIO else ''

for nome in ['index.html', 'obrigado.html']:
    s = open(os.path.join(AQUI, 'src', nome)).read()
    for marca, html in PARTES.items():
        s = s.replace(marca, html)
    s = (s.replace('<!--LOGO_DEFS-->', defs + (FOLHA_DEFS if nome == 'index.html' else '')).replace('<!--WA-->', WA).replace('<!--SETA-->', SETA)
          .replace('<!--CANONICAL-->', canonical).replace('<!--DOMINIO-->', DOMINIO))
    open(os.path.join(AQUI, nome), 'w').write(s)
    print('ok', nome, len(s), 'bytes')
