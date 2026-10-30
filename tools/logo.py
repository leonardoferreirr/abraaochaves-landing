"""Gera partials/logo-defs.html a partir do traço do logo (potrace) em tools/logo-groups.json.

Peças: árvore + caminho esquerdo, caminho direito, anel da rosa dos ventos, estrela,
"Abraão", "Chaves" e "LOGOTERAPEUTA". Coordenadas no espaço do traço (viewBox 2495x2265).
"""
import json, os, re

AQUI = os.path.dirname(os.path.abspath(__file__))
g = json.load(open(os.path.join(AQUI, 'logo-groups.json')))

PECAS = {
    'lg-tree': [0, 1],
    'lg-road': [6],
    'lg-ring': [4, 5, 7, 8],   # os 4 arcos do anel
    'lg-star': [2, 3],         # estrela de 8 pontas + ponto central
    'lg-abraao': list(range(9, 16)),
    'lg-chaves': list(range(16, 22)),
    'lg-sub': list(range(22, 35)),
}

def limpa(d):
    return re.sub(r'\s+', ' ', d).strip()

saida = ['<svg class="defs" aria-hidden="true" focusable="false"><defs>']
for nome, ks in PECAS.items():
    paths = ''.join(f'<path d="{limpa(g[k]["d"])}"/>' for k in ks)
    saida.append(f'<g id="{nome}"><g transform="translate(0 2265) scale(.1 -.1)">{paths}</g></g>')
saida.append('</defs></svg>')
os.makedirs(os.path.join(AQUI, '..', 'partials'), exist_ok=True)
open(os.path.join(AQUI, '..', 'partials', 'logo-defs.html'), 'w').write(''.join(saida))

# favicon: só o símbolo, quadrado
simb = ''.join(f'<path d="{limpa(g[k]["d"])}"/>' for n in ['lg-tree', 'lg-road', 'lg-ring', 'lg-star'] for k in PECAS[n])
fav = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="678 80 1170 1170">'
       '<style>path{fill:#5e6e38}@media (prefers-color-scheme:dark){path{fill:#c9dca6}}</style>'
       f'<g transform="translate(0 2265) scale(.1 -.1)">{simb}</g></svg>')
open(os.path.join(AQUI, '..', 'favicon.svg'), 'w').write(fav)
print('ok', sum(len(s) for s in saida), 'bytes de defs')
