"""Monta index.html e obrigado.html a partir de src/ e gera o que buscadores e
assistentes de IA leem: título, descrição, canonical, Open Graph, schema
(JSON-LD), robots.txt, sitemap.xml e llms.txt.

Uso: python3 build.py   (roda tools/logo.py antes se o traço do logo mudar)

O domínio mora só em DOMINIO. Para trocar de endereço, veja o README
("Como trocar de domínio sem perder SEO"): troque a constante, rode o build e o
.vercel.app ganha um redirect permanente para o domínio novo no vercel.json.

Os passos, as situações, as facetas, os serviços para empresas e o livro do
schema e do llms.txt são lidos do próprio src/index.html: editou a página,
rodou o build, os dois acompanham.
"""
import json, os, random, re
from datetime import date
from html import unescape

DOMINIO = 'https://abraaochaves.vercel.app'  # trocar quando houver domínio próprio (sem barra no fim)
VERCEL = 'abraaochaves.vercel.app'           # endereço da Vercel; ganha redirect quando DOMINIO for outro

NOME = 'Abraão Chaves'
FONE = '+55 91 8063-2788'            # o mesmo número do rodapé e do wa.me do obrigado.html
FONE_VER = '(91) 8063-2788'
INSTAGRAM = 'https://www.instagram.com/abraaochavess/'

# o que vai para o Google (título e descrição) e para o compartilhamento
TITULO = 'Logoterapeuta online | Abraão Chaves, filósofo e escritor'
DESCRICAO = ('Logoterapia online com Abraão Chaves, filósofo e escritor: sessões por vídeo para encontrar '
             'sentido, direção e equilíbrio. Palestras sobre NR-1 para empresas.')
OG_TITULO = 'Abraão Chaves | Logoterapeuta, filósofo e escritor'
OG_DESCRICAO = 'Te ajudo a encontrar sentido, direção e equilíbrio para a vida. Atendimento on-line, palestras e livros.'
OG_IMAGEM = '/assets/img/og.jpg'     # 1200 x 630
OG_ALT = 'Abraão Chaves, logoterapeuta, filósofo e escritor'

AQUI =os.path.dirname(os.path.abspath(__file__))
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
# ------------------------------------------------------------ busca e IA
def texto(frag):
    return re.sub(r'\s+', ' ', unescape(re.sub(r'<[^>]+>', '', frag))).strip()


def secao(html, id_):
    """Do id pedido até o fim da <section> em que ele está."""
    ini = html.index(f'id="{id_}"')
    return html[ini:html.index('</section>', ini)]


def lead(trecho):
    return texto(re.search(r'<p class="lead[^"]*"[^>]*>(.*?)</p>', trecho, flags=re.S).group(1))


def conteudo(html):
    """O que a página diz, lido dela mesma."""
    atend, sobre, livro, empresas = (secao(html, i) for i in ('atendimento', 'sobre', 'livro', 'empresas'))
    return {
        'situacoes': [texto(s) for t in re.findall(r'<div class="trilho">(.*?)</div>', atend, flags=re.S)
                      for s in re.findall(r'<span>(.*?)</span>', t)],
        'logoterapia': texto(re.search(r'<p class="grande[^"]*">(.*?)</p>', atend, flags=re.S).group(1)),
        'sessoes': [texto(p) for p in re.findall(r'<div class="corpo[^"]*"[^>]*>(.*?)<a ', atend, flags=re.S)[0].split('</p>') if texto(p)],
        'como': lead(secao(html, 'h-como')),
        'passos': [(texto(a), texto(b)) for a, b in re.findall(r'<li class="passo">.*?<h3>(.*?)</h3><p>(.*?)</p>', secao(html, 'h-como'))],
        'sobre': lead(sobre),
        'facetas': [(texto(a), texto(b)) for a, b in re.findall(r'<li class="faceta"><h3>(.*?)</h3>.*?<p>(.*?)</p>', sobre)],
        'livro_titulo': texto(re.search(r'<h2 id="h-livro"[^>]*>(.*?)</h2>', livro).group(1)),
        'livro': lead(livro),
        'empresas': lead(empresas),
        'servicos': [(texto(a), texto(b)) for a, b in re.findall(r'<li class="servico[^>]*><b>\d+</b><h3>(.*?)</h3><p>(.*?)</p>', empresas)],
    }


# nome completo de cada serviço para empresas no schema (na página o título é curto)
NOME_SERVICO = {
    'Diagnóstico': 'Diagnóstico de riscos psicossociais (NR-1)',
    'Palestras': 'Palestras sobre saúde mental e propósito',
    'Treinamentos': 'Treinamentos para equipes e liderança',
    'Planos de ação': 'Planos de ação de prevenção para empresas',
    'Comunicação e oratória': 'Aulas de comunicação e oratória',
}


def schema(c):
    S = DOMINIO
    eu, atende = {'@id': f'{S}/#abraao'}, {'@id': f'{S}/#atendimento'}
    servico = lambda nome, desc, tipo: {'@type': 'Offer', 'itemOffered': {
        '@type': 'Service', 'name': nome, 'description': desc, 'serviceType': tipo, 'provider': eu}}
    individual = servico('Atendimento on-line de logoterapia', c['passos'][-1][1], 'Logoterapia')
    individual['itemOffered']['availableChannel'] = {'@type': 'ServiceChannel', 'name': 'Sessões on-line por vídeo',
                                                     'servicePhone': {'@type': 'ContactPoint', 'telephone': FONE}}
    grafo = [
        {'@type': 'Person', **eu, 'name': NOME, 'url': f'{S}/', 'image': f'{S}/assets/img/abraao-retrato.webp',
         'jobTitle': [t for t, _ in c['facetas']],
         'description': 'Logoterapeuta, filósofo, escritor e palestrante, concluindo a formação em Psicanálise. '
                        'Atende on-line, por vídeo, e dá aulas de Comunicação e Oratória.',
         'knowsAbout': ['Logoterapia', 'Viktor Frankl', 'Saúde mental', 'Sentido de vida', 'Filosofia',
                        'Riscos psicossociais', 'NR-1', 'Comunicação e oratória'],
         'knowsLanguage': 'pt-BR', 'telephone': FONE, 'sameAs': [INSTAGRAM]},
        {'@type': 'ProfessionalService', **atende, 'name': f'{NOME}, logoterapeuta',
         'description': 'Atendimento on-line de logoterapia, por vídeo, com foco em saúde mental, e palestras, '
                        'treinamentos e diagnóstico de riscos psicossociais (NR-1) para empresas.',
         'url': f'{S}/', 'image': f'{S}{OG_IMAGEM}', 'telephone': FONE,
         'address': {'@type': 'PostalAddress', 'addressCountry': 'BR'},
         'founder': eu, 'knowsLanguage': 'pt-BR', 'sameAs': [INSTAGRAM],
         'hasOfferCatalog': {'@type': 'OfferCatalog', 'name': 'Atendimento, palestras e treinamentos',
                             'itemListElement': [individual] + [servico(NOME_SERVICO.get(n, n), d,
                                                                        'Comunicação e oratória' if 'oratória' in n.lower() else 'Saúde mental no trabalho')
                                                                for n, d in c['servicos']]}},
        {'@type': 'Book', '@id': f'{S}/#livro', 'name': c['livro_titulo'], 'author': eu, 'inLanguage': 'pt-BR',
         'url': f'{S}/#livro', 'image': f'{S}/assets/img/livro-capa.webp',
         'description': 'Livro de Abraão Chaves com reflexões sobre fé, dor, saudade, superação e o sentido da vida.'},
        {'@type': 'WebSite', '@id': f'{S}/#site', 'url': f'{S}/', 'name': NOME, 'inLanguage': 'pt-BR', 'publisher': eu},
        {'@type': 'WebPage', '@id': f'{S}/#pagina', 'url': f'{S}/', 'name': TITULO, 'description': DESCRICAO,
         'isPartOf': {'@id': f'{S}/#site'}, 'about': eu, 'mainEntity': eu, 'inLanguage': 'pt-BR',
         'primaryImageOfPage': {'@type': 'ImageObject', 'url': f'{S}{OG_IMAGEM}', 'width': 1200, 'height': 630}},
    ]
    js = json.dumps({'@context': 'https://schema.org', '@graph': grafo}, ensure_ascii=False, separators=(',', ':'))
    return '<script type="application/ld+json">' + js.replace('</', '<\\/') + '</script>'


def cabeca():
    a = lambda v: v.replace('&', '&amp;').replace('"', '&quot;')
    url, img = f'{DOMINIO}/', f'{DOMINIO}{OG_IMAGEM}'
    return '\n'.join([
        f'<title>{TITULO}</title>',
        f'<meta name="description" content="{a(DESCRICAO)}">',
        '<meta name="robots" content="index, follow, max-image-preview:large">',
        f'<meta name="author" content="{NOME}">',
        f'<link rel="canonical" href="{url}">',
        '<meta property="og:type" content="profile">',
        '<meta property="og:locale" content="pt_BR">',
        f'<meta property="og:site_name" content="{NOME}">',
        f'<meta property="og:url" content="{url}">',
        f'<meta property="og:title" content="{a(OG_TITULO)}">',
        f'<meta property="og:description" content="{a(OG_DESCRICAO)}">',
        f'<meta property="og:image" content="{img}">',
        '<meta property="og:image:width" content="1200">',
        '<meta property="og:image:height" content="630">',
        f'<meta property="og:image:alt" content="{a(OG_ALT)}">',
        '<meta property="profile:first_name" content="Abraão">',
        '<meta property="profile:last_name" content="Chaves">',
        '<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:title" content="{a(OG_TITULO)}">',
        f'<meta name="twitter:description" content="{a(OG_DESCRICAO)}">',
        f'<meta name="twitter:image" content="{img}">',
    ])


def llms(c):
    S = DOMINIO
    lin = [f'# {NOME}', '',
           f'> Logoterapeuta, filósofo, escritor e palestrante. Atende on-line, por vídeo, quem quer encontrar sentido, '
           f'direção e equilíbrio para a vida. Contato pelo WhatsApp {FONE_VER}.', '',
           '## Quem é', '',
           f'{NOME} é logoterapeuta, está concluindo a formação em Psicanálise e também é filósofo, escritor, '
           'palestrante e professor de Comunicação e Oratória. No Instagram, @abraaochavess.', '',
           f'Como ele se apresenta no site: “{c["sobre"]}”', '']
    lin += [f'- **{n}:** {d}' for n, d in c['facetas']]
    lin += ['', '## Atendimento individual', '',
            '- Formato: ' + c['como'],
            f'- Logoterapia: {c["logoterapia"]}']
    lin += [f'- {p}' for p in c['sessoes']]
    lin += ['- Preço das sessões: não é publicado no site.', '', '### Situações que levam alguém a buscar ajuda', '']
    lin += [f'- {s}' for s in c['situacoes']]
    lin += ['', '### Como funciona', '']
    lin += [f'{i}. **{n}.** {t}' for i, (n, t) in enumerate(c['passos'], 1)]
    lin += ['', '## Para empresas', '', f'Palestras, treinamentos e apoio às empresas na NR-1. No site: “{c["empresas"]}”', '']
    lin += [f'- **{NOME_SERVICO.get(n, n)}:** {d}' for n, d in c['servicos']]
    lin += ['', f'## Livro: {c["livro_titulo"]}', '', f'Livro de {NOME}. No site: “{c["livro"]}”', '',
            '## Contato', '',
            f'- WhatsApp: {FONE_VER} ({FONE})',
            f'- Agendar uma conversa: {S}/obrigado.html?c=llms',
            f'- Instagram: {INSTAGRAM}',
            f'- Site: {S}/', '']
    return '\n'.join(lin)


def redirecionar_vercel():
    """Com domínio próprio, o .vercel.app vira cópia da página. O redirect
    permanente (308, que o Google trata como 301) evita dois endereços no índice."""
    arq = os.path.join(AQUI, 'vercel.json')
    atual = open(arq).read()
    cfg = json.loads(atual)
    outros = [r for r in cfg.get('redirects', []) if not any(h.get('value') == VERCEL for h in r.get('has', []))]
    if VERCEL not in DOMINIO:
        host = [{'type': 'host', 'value': VERCEL}]
        # a raiz vai à parte: na Vercel o "/:path*" não pega a página inicial
        outros += [{'source': '/', 'has': host, 'destination': f'{DOMINIO}/', 'permanent': True},
                   {'source': '/:path*', 'has': host, 'destination': f'{DOMINIO}/:path*', 'permanent': True}]
    if outros:
        cfg['redirects'] = outros
    else:
        cfg.pop('redirects', None)
    novo = json.dumps(cfg, ensure_ascii=False, indent=2) + '\n'
    if json.loads(novo) != json.loads(atual):
        open(arq, 'w').write(novo)


# ------------------------------------------------------------ montagem
mudou = False
for nome in ['index.html', 'obrigado.html']:
    s = open(os.path.join(AQUI, 'src', nome)).read()
    for marca, html in PARTES.items():
        s = s.replace(marca, html)
    s = (s.replace('<!--LOGO_DEFS-->', defs + (FOLHA_DEFS if nome == 'index.html' else '')).replace('<!--WA-->', WA).replace('<!--SETA-->', SETA)
          .replace('<!--DOMINIO-->', DOMINIO))
    if nome == 'index.html':
        c = conteudo(s)
        s = re.sub(r'<!--SEO:[^>]*-->', lambda m: cabeca(), s).replace('<!--SCHEMA-->', schema(c))
    destino = os.path.join(AQUI, nome)
    if not os.path.exists(destino) or open(destino).read() != s:
        mudou = mudou or nome == 'index.html'
        open(destino, 'w').write(s)
    print('ok', nome, len(s), 'bytes')

open(os.path.join(AQUI, 'robots.txt'), 'w').write(
    '# Buscadores e assistentes de IA podem ler o site inteiro.\n'
    '# A obrigado.html fica fora do índice pelo noindex dela, não por aqui.\n'
    f'User-agent: *\nAllow: /\n\nSitemap: {DOMINIO}/sitemap.xml\n')

mapa = os.path.join(AQUI, 'sitemap.xml')
antes = re.search(r'<lastmod>([\d-]+)</lastmod>', open(mapa).read()) if os.path.exists(mapa) else None
dia = date.today().isoformat() if mudou or not antes else antes.group(1)
open(mapa, 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                      f'  <url><loc>{DOMINIO}/</loc><lastmod>{dia}</lastmod></url>\n</urlset>\n')

open(os.path.join(AQUI, 'llms.txt'), 'w').write(llms(c))
redirecionar_vercel()
print(f'robots.txt, sitemap.xml ({dia}) e llms.txt gerados para {DOMINIO}')
