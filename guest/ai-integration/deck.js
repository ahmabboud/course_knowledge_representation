/* AI Integration in the Market · slide engine and flow renderer.
   Keys: Right/Space next step · Left back · Home/End · N notes · F fullscreen.
   Any element with data-step="n" appears at step n (class .on; .now while n is current).
   Elements with class .cap show only while their step is current. */
(function () {
  'use strict';
  var NS = 'http://www.w3.org/2000/svg';
  var COLORS = { source: '--cyan', ai: '--green', human: '--violet', data: '--grey', knowledge: '--amber' };
  var NAMES = { source: 'Source team', ai: 'AI component', human: 'Person', data: 'File or data', knowledge: 'Expert knowledge' };
  function css(v) { return getComputedStyle(document.documentElement).getPropertyValue(v).trim(); }
  function mk(tag, attrs, parent) {
    var e = document.createElementNS(NS, tag);
    for (var k in attrs) e.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(e);
    return e;
  }

  /* ---------------------------------------------------------------- flows */
  function side(n, s) {
    if (s === 'top') return [n.x, n.y - n.h / 2];
    if (s === 'bottom') return [n.x, n.y + n.h / 2];
    if (s === 'left') return [n.x - n.w / 2, n.y];
    return [n.x + n.w / 2, n.y];
  }
  function sides(a, b) {
    var dx = b.x - a.x, dy = b.y - a.y;
    if (Math.abs(dx) * 0.6 > Math.abs(dy)) return dx > 0 ? ['right', 'left'] : ['left', 'right'];
    return dy > 0 ? ['bottom', 'top'] : ['top', 'bottom'];
  }
  function renderFlow(host) {
    var spec = JSON.parse(host.querySelector('script').textContent);
    var svg = mk('svg', { viewBox: '0 0 ' + spec.width + ' ' + spec.height, role: 'img', 'aria-label': spec.label || 'diagram' });
    var defs = mk('defs', {}, svg);
    var m = mk('marker', { id: 'ah' + Math.random().toString(36).slice(2), viewBox: '0 0 10 10', refX: 9, refY: 5, markerWidth: 7, markerHeight: 7, orient: 'auto-start-reverse' }, defs);
    mk('path', { d: 'M0,0 L10,5 L0,10 z', fill: css('--grey') }, m);
    var byId = {}, used = {};
    spec.nodes.forEach(function (n) { byId[n.id] = n; });
    var gE = mk('g', {}, svg), gN = mk('g', {}, svg), gB = mk('g', {}, svg);
    spec.edges.forEach(function (e) {
      var a = byId[e.from], b = byId[e.to], s = e.sides || sides(a, b);
      var p1 = side(a, s[0]), p2 = side(b, s[1]);
      var d = 'M' + p1[0] + ',' + p1[1];
      if (s[0] === 'right' || s[0] === 'left') {
        if (Math.abs(p1[1] - p2[1]) < 2) d += ' L' + p2[0] + ',' + p2[1];
        else { var mx = (p1[0] + p2[0]) / 2; d += ' C' + mx + ',' + p1[1] + ' ' + mx + ',' + p2[1] + ' ' + p2[0] + ',' + p2[1]; }
      } else {
        if (Math.abs(p1[0] - p2[0]) < 2) d += ' L' + p2[0] + ',' + p2[1];
        else { var my = (p1[1] + p2[1]) / 2; d += ' C' + p1[0] + ',' + my + ' ' + p2[0] + ',' + my + ' ' + p2[0] + ',' + p2[1]; }
      }
      var g = mk('g', { 'class': 'ed', 'data-step': e.step || 0 }, gE);
      mk('path', { d: d, 'marker-end': 'url(#' + m.id + ')' }, g);
      if (e.label) {
        var t = mk('text', { x: (p1[0] + p2[0]) / 2 + (e.dx || 12), y: (p1[1] + p2[1]) / 2 + (e.dy || -10), 'text-anchor': 'start' }, g);
        t.textContent = e.label;
      }
    });
    spec.nodes.forEach(function (n) {
      var col = css(COLORS[n.type] || '--grey'); used[n.type] = 1;
      var g = mk('g', { 'class': 'nd', 'data-step': n.step || 0 }, gN);
      mk('rect', { x: n.x - n.w / 2, y: n.y - n.h / 2, width: n.w, height: n.h, rx: 14,
        fill: n.type === 'ai' ? 'rgba(143,209,79,.12)' : css('--panel2'), stroke: col }, g);
      var lines = n.label.split('\n'), lh = 27, y0 = n.y - (lines.length - 1) * lh / 2;
      lines.forEach(function (ln, i) {
        var t = mk('text', { x: n.x, y: y0 + i * lh, 'text-anchor': 'middle', 'dominant-baseline': 'middle' }, g);
        t.textContent = ln;
      });
      [['pain', '--red', 'pain point'], ['flag', '--amber', null]].forEach(function (f) {
        if (!n[f[0]]) return;
        var txt = n[f[0] + 'Text'] || f[2] || 'note', st = n[f[0]];
        var bg = mk('g', { 'class': 'badge', 'data-step': st }, gB);
        mk('rect', { x: n.x - n.w / 2 - 4, y: n.y - n.h / 2 - 4, width: n.w + 8, height: n.h + 8, rx: 17, fill: 'none', stroke: css(f[1]), 'stroke-width': 3, 'stroke-dasharray': '8 6' }, bg);
        var w = txt.length * 11 + 28, bx = n.x + n.w / 2 - w, by = n.y - n.h / 2 - 18;
        mk('rect', { x: bx, y: by, width: w, height: 30, rx: 15, fill: css(f[1]) }, bg);
        var t = mk('text', { x: bx + w / 2, y: by + 16, 'text-anchor': 'middle', 'dominant-baseline': 'middle' }, bg);
        t.textContent = txt;
      });
    });
    host.insertBefore(svg, host.firstChild);
    if (spec.legend !== false) {
      var lg = document.createElement('div'); lg.className = 'legend';
      Object.keys(used).forEach(function (k) {
        lg.insertAdjacentHTML('beforeend', '<span><i style="border-color:' + css(COLORS[k]) + '"></i>' + NAMES[k] + '</span>');
      });
      if (spec.nodes.some(function (n) { return n.pain; })) lg.insertAdjacentHTML('beforeend', '<span><i style="border-color:' + css('--red') + ';border-style:dashed"></i>Pain point</span>');
      host.appendChild(lg);
    }
  }

  /* ---------------------------------------------------------------- deck */
  var slides = [], cur = 0, step = 0, deck, drawer;
  function maxStep(s) {
    var mx = 0;
    s.querySelectorAll('[data-step]').forEach(function (e) { mx = Math.max(mx, +e.getAttribute('data-step')); });
    return mx;
  }
  function paint() {
    slides.forEach(function (s, i) { s.classList.toggle('active', i === cur); });
    var s = slides[cur];
    s.querySelectorAll('[data-step]').forEach(function (e) {
      var n = +e.getAttribute('data-step');
      e.classList.toggle('on', step >= n);
      e.classList.toggle('now', step === n);
    });
    s.querySelector('.foot .n').textContent = (cur + 1) + ' / ' + slides.length;
    s.querySelector('.bar').style.width = ((cur + 1) / slides.length * 100) + '%';
    var notes = s.querySelector('.notes');
    drawer.innerHTML = '<b>Slide ' + (cur + 1) + ' · notes</b>' + (notes ? notes.innerHTML : '<p>No notes.</p>');
    history.replaceState(null, '', '#/' + (cur + 1) + (step ? '/' + step : ''));
  }
  function go(i, st) { cur = Math.max(0, Math.min(slides.length - 1, i)); step = st == null ? 0 : st; paint(); }
  function next() { if (step < maxStep(slides[cur])) { step++; paint(); } else if (cur < slides.length - 1) go(cur + 1, 0); }
  function prev() { if (step > 0) { step--; paint(); } else if (cur > 0) go(cur - 1, maxStep(slides[cur - 1])); }
  function fit() {
    var k = Math.min(window.innerWidth / 1600, window.innerHeight / 900);
    deck.style.transform = 'translate(-50%,-50%) scale(' + k + ')';
  }
  function boot() {
    deck = document.querySelector('.deck');
    slides = [].slice.call(document.querySelectorAll('.slide'));
    document.querySelectorAll('.flow').forEach(renderFlow);
    var course = document.body.getAttribute('data-footer') || '';
    slides.forEach(function (s) {
      s.insertAdjacentHTML('beforeend', '<div class="foot"><span>' + course + '</span><span class="n"></span></div><div class="bar"></div>');
    });
    drawer = document.createElement('div'); drawer.id = 'drawer'; document.body.appendChild(drawer);
    var nav = document.createElement('div'); nav.id = 'nav';
    nav.innerHTML = '<button data-a="prev">Back</button><button data-a="next">Next</button><button data-a="notes">Notes (N)</button><button data-a="full">Full screen (F)</button>';
    document.body.appendChild(nav);
    nav.addEventListener('click', function (e) {
      var a = e.target.getAttribute('data-a');
      if (a === 'prev') prev(); if (a === 'next') next();
      if (a === 'notes') drawer.classList.toggle('open');
      if (a === 'full') full();
    });
    document.addEventListener('keydown', function (e) {
      if (['ArrowRight', ' ', 'PageDown', 'Enter'].indexOf(e.key) >= 0) { e.preventDefault(); next(); }
      else if (['ArrowLeft', 'PageUp', 'Backspace'].indexOf(e.key) >= 0) { e.preventDefault(); prev(); }
      else if (e.key === 'Home') go(0); else if (e.key === 'End') go(slides.length - 1);
      else if (e.key === 'n' || e.key === 'N') drawer.classList.toggle('open');
      else if (e.key === 'f' || e.key === 'F') full();
    });
    window.addEventListener('resize', fit); fit();
    window.addEventListener('hashchange', function () {
      var m = location.hash.match(/#\/(\d+)(?:\/(\d+))?/);
      if (m && (+m[1] - 1 !== cur || +(m[2] || 0) !== step)) go(+m[1] - 1, m[2] ? +m[2] : 0);
    });
    var h = location.hash.match(/#\/(\d+)(?:\/(\d+))?/);
    go(h ? +h[1] - 1 : 0, h && h[2] ? +h[2] : 0);
    window.Deck = { go: go, next: next, count: slides.length };
  }
  function full() { if (!document.fullscreenElement) document.documentElement.requestFullscreen(); else document.exitFullscreen(); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
})();
