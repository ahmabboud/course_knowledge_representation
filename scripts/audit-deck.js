/* audit-deck.js — paste into the browser console on any lecture page.
 *
 * Every defect this repository shipped in its first month was invisible in the
 * HTML source and obvious the moment something rendered and got measured.
 * Structural checks (tags balanced, attributes present, ids unique) caught
 * none of them. This does the measuring.
 *
 *   1. Open the lecture over http (not file://).
 *   2. Add ?cb=<anything> to the URL. Without it a service worker or the
 *      HTTP cache can serve you a version that is not the one on disk, and
 *      you will spend an hour measuring the wrong page. This has happened.
 *   3. Clear this deck's saved state, or a restored answer inflates a slide:
 *        Object.keys(localStorage).filter(k=>k.startsWith('lu:')).forEach(k=>localStorage.removeItem(k))
 *      then reload.
 *   4. Paste this file. Read the report.
 *
 * Units: .slide is a fixed 1600x900 canvas that the runtime scales to the
 * window. getBoundingClientRect() returns SCALED pixels; clientHeight and
 * scrollHeight return UNSCALED canvas pixels. Mixing them silently inflates
 * every number by 1/scale. Everything below is reported in canvas pixels.
 */
(async function auditDeck() {
  const slides = [...document.querySelectorAll('.slide')];
  if (!slides.length || !window.LUDeck) { console.error('Not a lecture page, or the runtime has not booted.'); return; }
  const go = (n) => window.LUDeck.go(n);
  const sleep = (ms) => new Promise(r => setTimeout(r, ms));
  const stageScale = (() => {
    const m = getComputedStyle(document.querySelector('.deck__stage')).transform.match(/matrix\(([\d.]+)/);
    return m ? parseFloat(m[1]) : 1;
  })();
  const canvasPx = (screenPx) => Math.round(screenPx / stageScale);

  const report = { overflow: [], revealedOverflow: [], hiddenLeaks: [], gridEscapes: [], tinyText: [], collisions: [], edges: [] };

  /* 1. OVERFLOW — content taller than the slide box is clipped with no
        scrollbar and no error. Students simply never see it. */
  for (let i = 0; i < slides.length; i++) {
    go(i + 1); await sleep(90);
    const b = slides[i].querySelector('.slide__body'); if (!b) continue;
    const over = b.scrollHeight - b.clientHeight;
    if (over > 4) report.overflow.push({ slide: i + 1, label: slides[i].dataset.label, cutPx: over });
  }

  /* 2. OVERFLOW AFTER REVEAL — the state a slide is actually taught in.
        Every reveal open, every rationale shown. */
  document.querySelectorAll('.lu-reveal__panel, .lu-mcq__why').forEach(e => { e.hidden = false; });
  await sleep(200);
  for (let i = 0; i < slides.length; i++) {
    go(i + 1); await sleep(90);
    const b = slides[i].querySelector('.slide__body'); if (!b) continue;
    const over = b.scrollHeight - b.clientHeight;
    if (over > 4) report.revealedOverflow.push({ slide: i + 1, label: slides[i].dataset.label, cutPx: over });
  }

  /* 3. [hidden] THAT DOES NOT HIDE — a class rule setting `display` beats the
        UA [hidden] rule at equal-or-higher specificity. The element keeps its
        space, or renders on top of its siblings. Shipped twice here. */
  document.querySelectorAll('[hidden]').forEach(e => {
    if (getComputedStyle(e).display !== 'none') {
      report.hiddenLeaks.push({ cls: (typeof e.className === 'string' ? e.className : e.tagName), display: getComputedStyle(e).display });
    }
  });

  /* 4. GRID ESCAPES — a child of a narrow-first-column grid with no explicit
        grid-column lands in the narrow column and renders one word per line.
        This is what made .lu-mcq__why 44px wide and 462px tall. */
  document.querySelectorAll('.lu-mcq__opt, .lu-poll .lu-mcq__opt').forEach(opt => {
    const cs = getComputedStyle(opt);
    if (cs.display !== 'grid') return;
    const firstCol = parseFloat(cs.gridTemplateColumns);
    [...opt.children].forEach(c => {
      const w = c.getBoundingClientRect().width;
      if (w > 0 && canvasPx(w) <= firstCol + 6 && !c.classList.contains('lu-mcq__key')) {
        report.gridEscapes.push({ cls: c.className, widthPx: canvasPx(w), narrowColPx: firstCol });
      }
    });
  });

  /* 5. TEXT BELOW THE 20px PROJECTION FLOOR */
  document.querySelectorAll('.slide *').forEach(e => {
    if (!e.textContent.trim() || e.children.length) return;
    const fs = parseFloat(getComputedStyle(e).fontSize);
    if (fs && fs < 20) report.tinyText.push({ cls: (typeof e.className === 'string' ? e.className : e.tagName), fontSize: fs });
  });

  /* 6. DIAGRAM SANITY — nodes overlapping each other, and SVG edge endpoints
        that do not reach any node. Node positions are percentages and paths
        are viewBox units; setting them independently by eye does not work. */
  for (let i = 0; i < slides.length; i++) {
    const boards = slides[i].querySelectorAll('.lu-board');
    if (!boards.length) continue;
    go(i + 1); await sleep(90);
    for (const board of boards) {
      if (!board.offsetParent) continue;
      const nodes = [...board.querySelectorAll('.lu-node')].map(n => ({ r: n.getBoundingClientRect(), t: n.textContent.trim().slice(0, 18) }));
      for (let a = 0; a < nodes.length; a++) for (let c = a + 1; c < nodes.length; c++) {
        const A = nodes[a].r, B = nodes[c].r;
        if (A.left < B.right && B.left < A.right && A.top < B.bottom && B.top < A.bottom) {
          report.collisions.push({ slide: i + 1, pair: nodes[a].t + ' / ' + nodes[c].t });
        }
      }
      for (const p of board.querySelectorAll('path.lu-edge')) {
        const L = p.getTotalLength(); if (!L) continue;
        for (const pt of [p.getPointAtLength(0), p.getPointAtLength(L)]) {
          const sp = p.ownerSVGElement.createSVGPoint(); sp.x = pt.x; sp.y = pt.y;
          const s = sp.matrixTransform(p.getScreenCTM());
          let best = Infinity;
          for (const n of nodes) {
            const dx = Math.max(n.r.left - s.x, 0, s.x - n.r.right);
            const dy = Math.max(n.r.top - s.y, 0, s.y - n.r.bottom);
            best = Math.min(best, Math.hypot(dx, dy));
          }
          if (canvasPx(best) > 40) report.edges.push({ slide: i + 1, strayEndpointPx: canvasPx(best) });
        }
      }
    }
  }

  go(1);
  const fail = Object.values(report).some(v => v.length);
  console.log('%c=== DECK AUDIT ===', 'font-weight:bold');
  console.log('stage scale ' + stageScale.toFixed(3) + ', ' + slides.length + ' slides, numbers in canvas px');
  const show = (key, title, hint) => {
    if (!report[key].length) { console.log('%c  OK  ' + title, 'color:green'); return; }
    console.groupCollapsed('%c FAIL ' + title + ' (' + report[key].length + ')', 'color:#b00');
    console.table(report[key]); console.log(hint); console.groupEnd();
  };
  show('overflow', 'No slide overflows', 'Cut content is invisible and unscrollable. Shorten the TALL column of a two-column layout, or split the slide.');
  show('revealedOverflow', 'No slide overflows once revealed', 'This is the state you teach in. Shorten rationales and reveal panels.');
  show('hiddenLeaks', '[hidden] actually hides', 'A class rule is setting display and beating the UA [hidden] rule. Add a [hidden] companion, or do not set display at all.');
  show('gridEscapes', 'Nothing escaped into a narrow grid column', 'Give the child an explicit grid-column.');
  show('tinyText', 'No text below the 20px floor', 'Projection floor is --lu-t-caption.');
  show('collisions', 'No diagram nodes overlap', 'Reposition, or make the board taller.');
  show('edges', 'Every edge endpoint reaches a node', 'Compute path coords from node percentages: viewBox x = left% * (vbWidth/100), y = top% * (vbHeight/100).');
  console.log(fail ? '%cAudit FAILED. Fix the above before shipping.' : '%cAudit passed.', 'font-weight:bold;color:' + (fail ? '#b00' : 'green'));
  console.log('Not covered here, check by hand: print preview with Handout on, presenter view (P), study mode (S), and keyboard through every step.');
  return report;
})();
