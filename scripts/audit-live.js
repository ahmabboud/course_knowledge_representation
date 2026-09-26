/* audit-live.js: the live check used for Sessions 4 to 6 (2026-09-25).
   Paste into the console of a deployed deck (open it with ?cb=<commit> and
   clear this deck's lu: localStorage keys first), or run it through a browser
   tool. It walks every slide, steps every walkthrough to its last step, and
   stores the findings in window.__qa (an array of strings). When it finishes,
   window.__qa starts with "done"; an empty list after that means clean.

   What it catches, each a defect that has shipped and that scrollHeight
   alone misses:
     overflow        content taller than the slide
     into footer     content running over the footer line
     code over       a code line wider than its box (hidden, no scrollbar shows)
     table wider     a table wider than its column
     walk overlaps   a flow diagram running into its step bar
     badge / node outside canvas, label over a node, labels overlap
   It does not replace scripts/audit-deck.js, and it does not click MCQs:
   answer them by hand (or by script) from a clean state and re-check that slide.

   Study mode (S): the body scrolls in this mode instead of clipping content
   with no way to reach it (assets/lu.css, 2026-09-26), so the "overflow" and
   "into footer" checks are skipped while study mode is on; every other
   check still runs. Run this script once with study mode off (the baseline)
   and once with it on (AGENTS.md 2f).
*/
(async () => {
  window.__qa = ['running'];
  const sc = (() => { const m = getComputedStyle(document.querySelector('.deck__stage')).transform.match(/matrix\(([\d.]+)/); return m ? parseFloat(m[1]) : 1; })();
  const S = [...document.querySelectorAll('.slide')];
  const res = [];
  // Study mode inlines a definition after every glossary term a slide uses,
  // which can add more height than the fixed canvas holds; .slide__body
  // scrolls in that mode instead of clipping the content with no way to
  // reach it (assets/lu.css). A slide whose body is legitimately scrollable
  // is not a defect, so the two content-height checks below (raw overflow,
  // and content running into the footer) are skipped for it; every other
  // check (code width, table width, diagram geometry) still runs.
  const selfstudy = document.body.classList.contains('lu-selfstudy');
  const inter = (a, b, pad = 0) => a.left < b.right - pad && b.left < a.right - pad && a.top < b.bottom - pad && b.top < a.bottom - pad;
  const visible = el => getComputedStyle(el).opacity !== '0' && (!el.closest('g') || getComputedStyle(el.closest('g')).opacity !== '0');
  for (let n = 1; n <= S.length; n++) {
    window.LUDeck.go(n);
    await new Promise(r => setTimeout(r, 250));
    const s = S[n - 1], tag = `${n} ${s.dataset.label}:`;
    const w = s.querySelector('.lu-walk');
    if (w) {
      const next = [...w.querySelectorAll('button')].find(b => b.textContent.includes('Next step'));
      for (let k = 0; next && !next.disabled && k < 12; k++) { next.click(); await new Promise(r => setTimeout(r, 180)); }
      await new Promise(r => setTimeout(r, 500));
      const f = w.querySelector('.lu-flow'), bar = w.querySelector('.lu-walk__bar');
      if (f && bar && f.getBoundingClientRect().bottom > bar.getBoundingClientRect().top + 1)
        res.push(`${tag} walk overlaps bar by ${Math.round((f.getBoundingClientRect().bottom - bar.getBoundingClientRect().top) / sc)}px`);
    }
    if (!selfstudy && s.scrollHeight > s.clientHeight) res.push(`${tag} overflow ${s.scrollHeight - s.clientHeight}px`);
    for (const c of s.querySelectorAll('.lu-code pre')) if (c.scrollWidth > c.clientWidth + 1) res.push(`${tag} code over ${c.scrollWidth - c.clientWidth}px`);
    for (const t of s.querySelectorAll('table')) if (t.scrollWidth > t.parentElement.clientWidth + 1) res.push(`${tag} table wider by ${t.scrollWidth - t.parentElement.clientWidth}px`);
    const foot = s.querySelector('.slide__foot'), body = s.querySelector('.slide__body');
    if (!selfstudy && foot && body) {
      let mb = 0;
      for (const k of body.querySelectorAll('*')) { const r = k.getBoundingClientRect(); if (r.height > 0 && r.width > 0) mb = Math.max(mb, r.bottom); }
      if (mb > foot.getBoundingClientRect().top + 1) res.push(`${tag} into footer by ${Math.round((mb - foot.getBoundingClientRect().top) / sc)}px`);
    }
    for (const svg of s.querySelectorAll('.lu-flow svg')) {
      const sr = svg.getBoundingClientRect();
      const out = r => r.right > sr.right + 1 || r.bottom > sr.bottom + 1 || r.left < sr.left - 1 || r.top < sr.top - 1;
      const boxes = [...svg.querySelectorAll('.lu-flow__box')].filter(b => visible(b)).map(b => b.getBoundingClientRect());
      const labels = [...svg.querySelectorAll('text')].filter(t => !t.closest('.lu-flow__node') && t.textContent.trim() && visible(t)).map(t => ({ t: t.textContent, r: t.getBoundingClientRect() }));
      for (const g of svg.querySelectorAll('.lu-flow__flag')) if (visible(g) && out(g.getBoundingClientRect())) res.push(`${tag} badge outside canvas`);
      if ([...svg.querySelectorAll('.lu-flow__box')].some(b => out(b.getBoundingClientRect()))) res.push(`${tag} node outside canvas`);
      for (const l of labels) if (boxes.some(b => inter(l.r, b, 2))) res.push(`${tag} label "${l.t}" over a node`);
      for (let i = 0; i < labels.length; i++) for (let j = i + 1; j < labels.length; j++)
        if (inter(labels[i].r, labels[j].r, 2)) res.push(`${tag} labels "${labels[i].t}" and "${labels[j].t}" overlap`);
    }
  }
  window.__qa = ['done', ...res];
})();
