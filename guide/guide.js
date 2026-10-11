(function () {
  "use strict";
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  /* ---------- the system map ---------- */
  var LAYERS = [
    { id: "src", name: "Source data", sub: "Databases, files", tag: ["req", "Required"], st: "s1" },
    { id: "map", name: "Mapping", sub: "Rows become facts", tag: ["req", "If a database"], st: "s5" },
    { id: "graph", name: "RDF graph", sub: "Facts, linked", tag: ["req", "Required"], st: "s1" },
    { id: "vocab", name: "Vocabulary", sub: "RDFS, OWL", tag: ["opt", "RDFS almost always"], st: "s2" },
    { id: "shapes", name: "Shapes", sub: "SHACL rules", tag: ["opt", "Optional"], st: "s3" },
    { id: "prov", name: "History", sub: "Provenance, versions", tag: ["opt", "Optional"], st: "s4" },
    { id: "ask", name: "Questions", sub: "SPARQL, plain language", tag: ["opt", "Optional"], st: "s6" },
    { id: "ops", name: "Git, CI, containers", sub: "Keeps it working", tag: ["req", "In practice"], st: "s7" }
  ];
  var list = $("#layers");
  LAYERS.forEach(function (l) {
    var li = document.createElement("li");
    var b = document.createElement("button");
    b.type = "button"; b.className = "layer"; b.dataset.id = l.id;
    var left = document.createElement("span");
    var n = document.createElement("b"); n.textContent = l.name;
    var s = document.createElement("small"); s.textContent = l.sub;
    left.appendChild(n); left.appendChild(s);
    var t = document.createElement("span"); t.className = "tag tag--" + l.tag[0]; t.textContent = l.tag[1];
    b.appendChild(left); b.appendChild(t);
    b.addEventListener("click", function () {
      var el = document.getElementById(l.st); if (el) el.scrollIntoView({ block: "start" });
    });
    li.appendChild(b); list.appendChild(li);
  });

  var stations = $$(".station");
  var bar = $("#bar");
  function activate(idx) {
    var on = {}, now = {};
    stations.forEach(function (st, i) {
      var ids = (st.dataset.layers || "").split(",");
      ids.forEach(function (id) { if (i <= idx) on[id] = true; if (i === idx) now[id] = true; });
    });
    $$(".layer").forEach(function (b) {
      b.classList.toggle("is-on", !!on[b.dataset.id]);
      b.classList.toggle("is-now", !!now[b.dataset.id]);
    });
    bar.style.width = Math.round(((idx + 1) / (stations.length + 1)) * 100) + "%";
  }
  activate(0);
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) activate(stations.indexOf(e.target)); });
    }, { rootMargin: "-45% 0px -45% 0px", threshold: 0 });
    stations.forEach(function (s) { io.observe(s); });
    var build = document.getElementById("s8");
    new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { $$(".layer").forEach(function (b) { b.classList.add("is-on"); b.classList.remove("is-now"); }); bar.style.width = "100%"; } });
    }, { threshold: 0.15 }).observe(build);
  } else {
    $$(".layer").forEach(function (b) { b.classList.add("is-on"); });
  }

  /* ---------- helpers ---------- */
  function seg(ids, onpick) {
    ids.forEach(function (id) {
      var b = document.getElementById(id);
      b.addEventListener("click", function () {
        ids.forEach(function (o) { document.getElementById(o).setAttribute("aria-pressed", o === id ? "true" : "false"); });
        onpick(id);
      });
    });
  }
  function text(el, s) { el.textContent = s; }

  /* ---------- 1 table or graph ---------- */
  seg(["v-table", "v-graph"], function (id) {
    $("#p-table").hidden = id !== "v-table";
    $("#p-graph").hidden = id !== "v-graph";
  });

  /* ---------- 2 vocabulary ---------- */
  seg(["m-none", "m-voc"], function (id) {
    var withV = id === "m-voc";
    text($("#m-num"), withV ? "9,215" : "9,023");
    text($("#m-txt"), withV
      ? "With a vocabulary that says a late order is an order, the same question counts all 9,215."
      : "“How many orders?” counts only things typed Order. The 192 late orders are missed.");
    text($("#m-code"), withV
      ? "ul:LateOrder  rdfs:subClassOf  ul:Order .   # a late order is an order"
      : "ul:LateOrder  a rdfs:Class .   # a separate type");
  });

  /* ---------- 3 reasoner or validator ---------- */
  var tout = $("#t-out"), twrap = $("#t-code-wrap");
  var IO = {
    "t-owl": [["Takes in", "The RDF data graph, and the ontology (RDFS and OWL rules)."], ["Assumes", "Open world: a missing fact is unknown, not false."], ["Gives out", "New facts, or a contradiction. Never a list of broken rules."]],
    "t-shacl": [["Takes in", "The RDF data graph, and the shapes (rules, also written in RDF)."], ["Assumes", "Closed world: a missing fact is a problem."], ["Gives out", "A report: one result for each broken rule."]]
  };
  function tool(id) {
    var io = $("#t-io"); io.innerHTML = "";
    IO[id].forEach(function (r) { var d = document.createElement("div"); var b = document.createElement("b"); b.textContent = r[0]; d.appendChild(b); d.appendChild(document.createTextNode(r[1])); io.appendChild(d); });
    tout.innerHTML = "";
    var p = document.createElement("p"); p.style.margin = "0";
    if (id === "t-owl") {
      p.innerHTML = "<span class='unk'>No error.</span> Order 1447291369.7 has no carrier, so the reasoner treats it as <b>unknown</b>. A carrier probably exists somewhere. Missing is not false.";
      twrap.hidden = true;
    } else {
      p.innerHTML = "<span class='bad'>Violation.</span> MinCount on <code>ul:carriedBy</code>, for order 1447291369.7. The rule needs at least one carrier, and there are zero. The validator checks only the data it is given.";
      twrap.hidden = false;
    }
    tout.appendChild(p);
  }
  seg(["t-owl", "t-shacl"], tool); tool("t-owl");

  /* ---------- 4 provenance trail ---------- */
  var steps = [
    "<b>Fact:</b> order 1447336276.7 weighs 0 kg",
    "<b>Graph:</b> OrderList (119,844 triples)",
    "<b>File:</b> OrderList.csv, with its checksum",
    "<b>Run:</b> the Session 2 conversion, 2026-09-25 01:31 UTC",
    "<b>Program:</b> convert_to_rdf.py",
    "<b>Rules:</b> checked with shapes against ontology release 1.0.0"
  ];
  var tn = 0, trail = $("#trail"), tbtn = $("#trace");
  tbtn.addEventListener("click", function () {
    if (tn >= steps.length) { trail.innerHTML = ""; tn = 0; tbtn.textContent = "Trace order 1447336276.7"; return; }
    var li = document.createElement("li"); li.innerHTML = steps[tn]; trail.appendChild(li); tn++;
    tbtn.textContent = tn < steps.length ? "Next: where did that come from?" : "Start again";
  });

  /* ---------- 5 materialize or virtualize ---------- */
  var added = false;
  $("#newrow").addEventListener("click", function () {
    added = !added;
    text($("#mat"), "9,215"); text($("#mat-n"), added ? "stored graph: still the old snapshot, until you run it again" : "orders in the stored graph");
    text($("#vir"), added ? "9,216" : "9,215"); text($("#vir-n"), added ? "orders, asked just now: includes the new one" : "orders, asked just now");
    this.textContent = added ? "Reset" : "A new late order arrives in the database";
  });

  /* ---------- 6 plain-language questions ---------- */
  var QS = [
    { q: "How many orders did carrier V44_3 carry?", sparql: "SELECT (COUNT(?o) AS ?n) WHERE {\n  ?o ul:carriedBy <.../carrier/brunel/V44_3> }", ans: "854", note: "The check passed: every property exists. The query is the evidence." },
    { q: "How many orders are there in total?", sparql: "SELECT (COUNT(DISTINCT ?o) AS ?n) WHERE {\n  ?o a/rdfs:subClassOf* ul:Order }", ans: "9,215", note: "It follows the hierarchy from Question 2, so late orders count." },
    { q: "Which customers are in Beirut?", sparql: null, ans: "REFUSED", note: "The graph has no places at all. The right answer is a refusal that says what is missing, not a guess." }
  ];
  var qout = $("#q-out");
  function ask(i) {
    var o = QS[i]; qout.innerHTML = "";
    if (o.sparql) {
      var pre = document.createElement("pre"); pre.style.marginTop = "0"; pre.textContent = o.sparql; qout.appendChild(pre);
      var a = document.createElement("div"); a.className = "big"; a.style.marginTop = "10px"; a.textContent = o.ans; qout.appendChild(a);
    } else {
      var r = document.createElement("div"); r.className = "big"; r.textContent = "I cannot answer that."; qout.appendChild(r);
    }
    var n = document.createElement("p"); n.className = "foot"; n.textContent = o.note; qout.appendChild(n);
  }
  $$("[data-q]").forEach(function (b) {
    b.addEventListener("click", function () {
      $$("[data-q]").forEach(function (o) { o.setAttribute("aria-pressed", o === b ? "true" : "false"); });
      ask(+b.dataset.q);
    });
  });
  ask(0);

  /* ---------- 7 the gate ---------- */
  var gout = $("#g-out");
  function gate(id) {
    gout.innerHTML = "";
    var ok = id === "g-ok";
    var pill = document.createElement("span"); pill.className = "pill " + (ok ? "pill--g" : "pill--r"); pill.textContent = ok ? "Green" : "Red";
    var msg = document.createElement("span");
    msg.innerHTML = ok
      ? "<code>GATE: PASS, no violations.</code> The change can be merged."
      : "<code>GATE: FAIL, 1 violations. Exit code 1.</code> V444_O is not a Carrier, so the change is stopped.";
    gout.appendChild(pill); gout.appendChild(msg);
  }
  seg(["g-ok", "g-bad"], gate); gate("g-ok");

  /* ---------- 8 build your stack ---------- */
  var ORDER = [
    ["src", "Source data"], ["map", "Mapping"], ["graph", "RDF graph and triple store"], ["vocab", "Vocabulary (RDFS, OWL)"],
    ["shapes", "Shapes (SHACL)"], ["prov", "History (provenance, versions)"], ["ask", "Plain-language questions"], ["ops", "Git, CI, containers"]
  ];
  var stack = $("#stack"), note = $("#stack-note");
  function stackOf(n) {
    var s = { src: "need", ops: "need" };
    if (n.simple && !n.join && !n.reuse && !n.reason && !n.quality && !n.trace) {
      return { s: { src: "need", ops: "need", graph: "skip", map: "skip", vocab: "skip", shapes: "skip", prov: "skip", ask: n.ask ? "maybe" : "skip" },
        msg: "A property graph database such as Neo4j may fit you better than the RDF stack. You keep git and CI, and you write your own checks and naming rules." };
    }
    s.graph = "need"; s.vocab = "maybe"; s.shapes = "maybe"; s.prov = "maybe"; s.map = "skip"; s.ask = "skip";
    if (n.join) { s.graph = "need"; s.vocab = "need"; }
    if (n.reuse || n.reason) { s.vocab = "need"; }
    if (n.quality) { s.shapes = "need"; }
    if (n.live) { s.map = "need"; }
    if (n.trace) { s.prov = "need"; }
    if (n.ask) { s.ask = "need"; }
    var msg = n.reason ? "Reasoning needs OWL and a reasoner. It is the layer teams use least in production, so confirm you need it." : "You can leave OWL reasoning out. RDFS plus SHACL covers most of what teams use.";
    return { s: s, msg: msg };
  }
  var LAB = { need: "Need", maybe: "Worth having", skip: "Skip for now" };
  function render() {
    var n = {};
    $$("#needs input").forEach(function (c) { n[c.dataset.n] = c.checked; });
    var any = Object.keys(n).some(function (k) { return n[k]; });
    stack.innerHTML = "";
    if (!any) {
      var li0 = document.createElement("li"); li0.textContent = "Tick at least one need on the left."; stack.appendChild(li0); note.textContent = ""; return;
    }
    var r = stackOf(n);
    ORDER.forEach(function (o) {
      var li = document.createElement("li"); var a = document.createElement("span"); a.textContent = o[1];
      var b = document.createElement("span"); var st = r.s[o[0]] || "skip"; b.className = "st st--" + st; b.textContent = LAB[st];
      li.appendChild(a); li.appendChild(b); stack.appendChild(li);
    });
    note.textContent = r.msg;
  }
  $$("#needs input").forEach(function (c) { c.addEventListener("change", render); });
  render();
})();
