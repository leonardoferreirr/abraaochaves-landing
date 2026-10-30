"""Gera os caminhos de fundo (SVG) em partials/raizes-*.html.

Estilo ilustrado, igual à estrada do "Como funciona" e ao caminho do logo: duas linhas
paralelas que descem em curva e vão se abrindo no fim, como estrada em perspectiva.
Cada linha leva data-i (quando começa a se desenhar, de 0 a 1) para o main.js desenhar
com a rolagem. Sem acaso: o desenho é sempre o mesmo.
"""
import math, os

AQUI = os.path.dirname(os.path.abspath(__file__))

def suave(pts):
    # Catmull-Rom para Bézier cúbica
    d = f'M{pts[0][0]:.1f} {pts[0][1]:.1f}'
    for i in range(len(pts) - 1):
        p0 = pts[i - 1] if i else pts[i]
        p1, p2 = pts[i], pts[i + 1]
        p3 = pts[i + 2] if i + 2 < len(pts) else p2
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f' C{c1[0]:.1f} {c1[1]:.1f} {c2[0]:.1f} {c2[1]:.1f} {p2[0]:.1f} {p2[1]:.1f}'
    return d

def caminho(x0, y0, y1, amp, onda, fase, abre0, abre1, deriva=0):
    """Duas bordas de uma estrada sinuosa: centro em senoide, largura crescendo."""
    centro = []
    n = max(8, int((y1 - y0) / 34))
    for k in range(n + 1):
        t = k / n
        y = y0 + (y1 - y0) * t
        x = x0 + deriva * t + amp * math.sin(2 * math.pi * (y - y0) / onda + fase) * (.35 + .65 * t)
        centro.append((x, y, t))
    bordas = ([], [])
    for i, (x, y, t) in enumerate(centro):
        xa, ya, _ = centro[max(0, i - 1)]
        xb, yb, _ = centro[min(len(centro) - 1, i + 1)]
        tx, ty = xb - xa, yb - ya
        L = math.hypot(tx, ty) or 1
        nx, ny = -ty / L, tx / L
        meia = (abre0 + (abre1 - abre0) * t ** 1.4) / 2
        bordas[0].append((x + nx * meia, y + ny * meia))
        bordas[1].append((x - nx * meia, y - ny * meia))
    return [suave(b) for b in bordas]

def gera(nome, W, H, estradas, traco):
    corpo = ''
    for (x0, y0, y1, amp, onda, fase, abre0, abre1, deriva, ini) in estradas:
        for d in caminho(x0, y0, y1, amp, onda, fase, abre0, abre1, deriva):
            corpo += f'<path d="{d}" stroke-width="{traco}" data-i="{ini:.2f}" pathLength="1"/>'
    svg = (f'<svg class="raizes" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMin slice" aria-hidden="true">'
           f'<g class="balanco">{corpo}</g></svg>')
    open(os.path.join(AQUI, '..', 'partials', f'raizes-{nome}.html'), 'w').write(svg)
    print(nome, len(estradas), 'caminhos,', len(svg), 'bytes')

# do pé do topo até a frase: dois caminhos largos nas laterais, um fino no meio (o que sobra no celular)
#            x0    y0  y1   amp  onda fase abre0 abre1 deriva ini
gera('frase', 1440, 820, [
    (250,   0, 820, 70, 520, 0.0, 6, 30, -60, .00),
    (1190,  0, 820, 80, 600, 2.4, 6, 30,  50, .08),
    (720, 120, 820, 46, 420, 1.2, 4, 18,  20, .30),
], 1.8)
# embaixo do livro: a terra do "Entre o Céu e a Terra"
gera('livro', 1440, 460, [
    (380,  0, 460, 60, 380, 0.6, 5, 26, -30, .00),
    (1080, 60, 460, 50, 340, 2.0, 4, 20,  40, .20),
], 1.5)
