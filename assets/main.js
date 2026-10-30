// Abraão Chaves: movimento da página. Sem bibliotecas; tudo em rAF + IntersectionObserver.
// Regra da casa: nada nasce invisível dependendo daqui. Se este arquivo falhar, a página aparece inteira.
(() => {
  const d = document, root = d.documentElement;
  const reduz = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const celular = () => innerWidth < 900;
  const lim = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
  const sai = t => 1 - Math.pow(1 - t, 3);
  const volta = t => { const c = 1.5; return 1 + (c + 1) * Math.pow(t - 1, 3) + c * Math.pow(t - 1, 2); };
  const $ = s => d.querySelector(s), $$ = s => [...d.querySelectorAll(s)];

  /* ---------- símbolo do topo: o caminho sobe até a árvore, a rosa dos ventos se acende ---------- */
  const simbolo = $('#simbolo'), cresce = $('#cresce'), anel = $('#anel'), estrela = $('#estrela');
  const CX = 1399.5, CY = 765;
  let introAcabou = false, heroNaTela = true;
  const poeEstrela = (ang, esc = 1) => estrela.setAttribute('transform',
    `rotate(${ang.toFixed(2)} ${CX} ${CY}) translate(${CX} ${CY}) scale(${esc.toFixed(3)}) translate(${-CX} ${-CY})`);

  if (simbolo) {
    if (reduz) {
      simbolo.classList.add('pronto'); introAcabou = true;
    } else {
      cresce.setAttribute('y', 1260);
      anel.setAttribute('stroke-dashoffset', 100);
      estrela.style.opacity = 0;
      simbolo.classList.add('pronto');
      const t0 = performance.now();
      const quadro = agora => {
        const t = (agora - t0) / 1000;
        cresce.setAttribute('y', (1260 - sai(lim(t / 2)) * 1520).toFixed(1));
        anel.setAttribute('stroke-dashoffset', (100 - sai(lim((t - .8) / 1.2)) * 100).toFixed(2));
        const e = lim((t - 1.1) / 1.3);
        estrela.style.opacity = lim(e * 3);
        poeEstrela(-150 * (1 - sai(e)) + scrollY * .14, .5 + .5 * volta(e));
        if (t < 2.5) requestAnimationFrame(quadro); else introAcabou = true;
      };
      requestAnimationFrame(quadro);
    }
  }

  /* ---------- frase acendendo palavra por palavra ---------- */
  const frase = $('#frase');
  let palavras = [];
  if (frase && !reduz) {
    const nos = [...frase.childNodes];
    frase.textContent = '';
    nos.forEach(no => {
      if (no.nodeType === 3) {
        no.textContent.split(/(\s+)/).forEach(p => {
          if (!p) return;
          if (/^\s+$/.test(p)) frase.append(p);
          else { const s = d.createElement('span'); s.className = 'w'; s.textContent = p; frase.append(s); }
        });
      } else { no.classList.add('w'); frase.append(no); }
    });
    palavras = $$('#frase .w');
    frase.closest('.frase').classList.add('vivo');
  }

  /* ---------- estrada dos passos ---------- */
  const passos = $('#passos'), estrada = $('#estrada');
  const itens = passos ? $$('#passos .passo') : [];
  let marcos = [];
  function tracaEstrada() {
    if (!estrada) return;
    const caixa = estrada.getBoundingClientRect();
    const w = caixa.width, h = passos.offsetHeight;
    estrada.setAttribute('viewBox', `0 0 ${w.toFixed(1)} ${h}`);
    estrada.setAttribute('width', w.toFixed(1)); estrada.setAttribute('height', h);
    const pts = itens.map(li => {
      const r = li.querySelector('.marco').getBoundingClientRect();
      return { x: r.left + r.width / 2 - caixa.left, y: r.top + r.height / 2 - caixa.top };
    });
    if (!pts.length) return;
    const A = celular() ? 26 : 22;
    const linha = dx => {
      let s = `M${(pts[0].x + dx).toFixed(1)} 0 L${(pts[0].x + dx).toFixed(1)} ${pts[0].y.toFixed(1)}`;
      for (let i = 0; i < pts.length; i++) {
        const a = pts[i], b = pts[i + 1] || { x: a.x, y: h };
        const dy = b.y - a.y, lado = i % 2 ? -A : A;
        s += ` C${(a.x + dx + lado).toFixed(1)} ${(a.y + dy * .35).toFixed(1)} ${(b.x + dx - lado).toFixed(1)} ${(a.y + dy * .65).toFixed(1)} ${(b.x + dx).toFixed(1)} ${b.y.toFixed(1)}`;
      }
      return s;
    };
    const ps = estrada.querySelectorAll('path');
    [-5, 5, -5, 5].forEach((dx, i) => ps[i].setAttribute('d', linha(dx)));
    ps[2].setAttribute('pathLength', 1); ps[3].setAttribute('pathLength', 1);
    ps[2].style.strokeDasharray = ps[3].style.strokeDasharray = '1 1';
    marcos = pts.map(p => p.y / h);
  }

  /* ---------- livro 3D ---------- */
  const palco = $('#palco'), livro = $('#b3d');
  let mira = { x: 0, y: 0 }, miraAlvo = { x: 0, y: 0 };
  if (palco && !reduz) {
    palco.addEventListener('pointermove', e => {
      if (e.pointerType !== 'mouse') return;
      const r = palco.getBoundingClientRect();
      miraAlvo = { x: (e.clientX - r.left) / r.width - .5, y: (e.clientY - r.top) / r.height - .5 };
      pede();
    });
    palco.addEventListener('pointerleave', () => { miraAlvo = { x: 0, y: 0 }; pede(); });
  }

  /* ---------- caminhos de fundo: cada linha se desenha a partir do seu data-i ---------- */
  const caminhos = $$('.raizes').map(svg => ({ svg, linhas: [...svg.querySelectorAll('path')].map(el => ({ el, i: +el.dataset.i, ult: -1 })) }));
  const folhas = $$('.folhas');
  function medeQueda() { folhas.forEach(f => f.style.setProperty('--queda', `${f.offsetHeight + 160}px`)); }

  /* ---------- um laço só para tudo que depende da rolagem ---------- */
  const topo = $('#topo');
  let pedido = false;
  function pede() { if (!pedido) { pedido = true; requestAnimationFrame(quadroRolagem); } }
  function quadroRolagem() {
    pedido = false;
    const vh = innerHeight, y = scrollY;
    topo.classList.toggle('solid', y > 24);

    if (introAcabou && heroNaTela && estrela && !reduz) poeEstrela(y * .14);

    if (palavras.length) {
      const r = frase.getBoundingClientRect();
      const p = lim((vh * .86 - r.top) / (r.height + vh * .36));
      const n = Math.round(p * palavras.length);
      palavras.forEach((w, i) => w.classList.toggle('on', i < n));
    }

    if (estrada && marcos.length && !reduz) {
      const r = passos.getBoundingClientRect();
      const p = lim((vh * .62 - r.top) / r.height);
      const ps = estrada.querySelectorAll('.viva');
      ps.forEach(el => { el.style.strokeDashoffset = (1 - p).toFixed(4); });
      itens.forEach((li, i) => li.classList.toggle('on', p >= marcos[i] - .02));
    } else if (estrada) itens.forEach(li => li.classList.add('on'));

    if (!reduz) caminhos.forEach(({ svg, linhas }) => {
      const r = svg.getBoundingClientRect();
      if (r.bottom < -50 || r.top > vh + 50) return;
      const p = lim((vh * .92 - r.top) / (r.height * .8));
      linhas.forEach(l => {
        const v = Math.round(lim((p - l.i * .7) / .55) * 1000) / 1000;
        if (v !== l.ult) { l.ult = v; l.el.style.strokeDashoffset = 1 - v; }
      });
    });

    if (livro && !reduz) {
      const r = palco.getBoundingClientRect();
      const p = lim((vh - r.top) / (vh + r.height));
      mira.x += (miraAlvo.x - mira.x) * .14; mira.y += (miraAlvo.y - mira.y) * .14;
      livro.style.setProperty('--ry', `${(-40 + p * 30 + mira.x * 18).toFixed(2)}deg`);
      livro.style.setProperty('--rx', `${(7 - p * 5 - mira.y * 12).toFixed(2)}deg`);
      if (Math.abs(miraAlvo.x - mira.x) + Math.abs(miraAlvo.y - mira.y) > .002) pede();
    }
  }
  addEventListener('scroll', pede, { passive: true });
  addEventListener('resize', () => { tracaEstrada(); medeQueda(); pede(); });

  /* ---------- observadores ---------- */
  if ('IntersectionObserver' in window) {
    const revela = new IntersectionObserver(es => es.forEach(e => {
      if (e.isIntersecting) { e.target.classList.add('in'); revela.unobserve(e.target); }
    }), { rootMargin: '0px 0px -8% 0px', threshold: .12 });
    $$('.rv').forEach(el => revela.observe(el));
    root.classList.add('rv-pronto');

    const hero = $('.hero');
    if (hero) new IntersectionObserver(([e]) => { heroNaTela = e.isIntersecting; }).observe(hero);

    // faceta acesa: a que cruza o meio da tela
    const facetas = $('#facetas');
    if (facetas && !reduz) {
      const fs = $$('#facetas .faceta');
      fs[0].classList.add('on');
      facetas.classList.add('vivo');
      const obsFaceta = new IntersectionObserver(es => es.forEach(e => {
        if (!e.isIntersecting) return;
        fs.forEach(f => f.classList.toggle('on', f === e.target));
      }), { rootMargin: '-44% 0px -44% 0px' });
      fs.forEach(f => obsFaceta.observe(f));
    }

    const servicos = $('#servicos');
    if (servicos && !reduz) servicos.classList.add('vivo');

    if (palco) new IntersectionObserver(([e]) => palco.classList.toggle('roda', e.isIntersecting)).observe(palco);

    // folhas e balanço dos caminhos só andam com a seção na tela
    const anda = new IntersectionObserver(es => es.forEach(e => e.target.classList.toggle('roda', e.isIntersecting && !reduz)));
    folhas.forEach(f => anda.observe(f));
    caminhos.forEach(c => anda.observe(c.svg));

    // barra do celular: aparece depois do topo e some no fechamento
    const barra = $('#barra'), acoesHero = $('#acoes-hero'), fim = $('.final');
    if (barra && acoesHero && fim) {
      let heroVisivel = true, fimVisivel = false;
      const ajusta = () => barra.classList.toggle('on', !heroVisivel && !fimVisivel && scrollY > 200);
      new IntersectionObserver(([e]) => { heroVisivel = e.isIntersecting; ajusta(); }).observe(acoesHero);
      new IntersectionObserver(([e]) => { fimVisivel = e.isIntersecting; ajusta(); }).observe(fim);
    }
  }

  /* ---------- faixas infinitas: copia até a metade passar da largura da tela ---------- */
  const faixas = $$('.faixa');
  const originais = new Map(faixas.map(f => [f, f.querySelector('.trilho').innerHTML]));
  function montaFaixa(f) {
    const trilho = f.querySelector('.trilho');
    trilho.innerHTML = originais.get(f);
    const umJogo = trilho.scrollWidth, tela = f.clientWidth;
    const k = Math.max(1, Math.ceil(tela / umJogo));
    trilho.innerHTML = originais.get(f).repeat(k * 2);
    trilho.style.setProperty('--dur', `${parseFloat(getComputedStyle(f).getPropertyValue('--dur')) * k}s`);
  }
  const obsFaixa = 'IntersectionObserver' in window
    ? new IntersectionObserver(es => es.forEach(e => e.target.classList.toggle('roda', e.isIntersecting && !reduz)))
    : null;
  const ocioso = window.requestIdleCallback || (fn => setTimeout(fn, 60));
  function montaFaixas() {
    faixas.forEach((f, i) => ocioso(() => { montaFaixa(f); if (obsFaixa) obsFaixa.observe(f); }));
  }

  /* ---------- partida ---------- */
  const comeca = () => { tracaEstrada(); medeQueda(); pede(); };
  comeca();
  d.fonts && d.fonts.ready.then(comeca);
  if (d.readyState === 'complete') montaFaixas();
  else addEventListener('load', () => { comeca(); montaFaixas(); });
  let tr; addEventListener('resize', () => { clearTimeout(tr); tr = setTimeout(() => faixas.forEach(montaFaixa), 250); });
})();
