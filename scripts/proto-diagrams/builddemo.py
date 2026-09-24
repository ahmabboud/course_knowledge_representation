"""Builds lectures/proto-diagrams.html: the lu-flow demo deck (design system v1.2)."""
import json
spec = open('/tmp/proto/spec.json').read().strip()
caps = [
 "<b>Step 1.</b> Our class says: an order for a sole-sourced good orders <b>some product</b>, and that product depends on a sole-sourced component.",
 "<b>Step 2.</b> The <b>domain</b> of dependsOnProduct is SupplyRelationship. So the reasoner concludes the product <b>is a supply relationship</b>.",
 "<b>Step 3.</b> In BFO, a supply relationship is a <b>specifically dependent continuant</b>: it only exists in other things, like a role.",
 "<b>Step 4.</b> But the product is a MaterialProduct, so a material entity, so an <b>independent continuant</b>: a thing that exists on its own.",
 "<b>Step 5.</b> BFO declares these two <b>disjoint</b>: nothing can be both. Our product would have to be both.",
 "<b>Step 6.</b> No such product can exist, so no such order can exist. The class is <b>equivalent to owl:Nothing</b>: the red line in Protégé.",
]
shorts = ["The class", "Domain", "BFO parent", "Other parent", "Disjoint", "Empty class"]
steps = "\n".join(f'        <div data-walk-step="{i+1}" data-caption-short="{shorts[i]}" data-caption="{c.replace(chr(34), "&quot;")}"></div>' for i, c in enumerate(caps))
HEAD = '''<!DOCTYPE html>
<html lang="en" class="lu-deck-page">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Flow diagrams · Knowledge Representation</title>
<meta name="description" content="The lu-flow diagram component: blocks and arrows from one spec, step-animated, with colours that name the ontology layer.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,500;0,8..60,600;1,8..60,400&family=IBM+Plex+Sans:ital,wght@0,400;0,500;0,600;1,400&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../assets/lu.css?v=1.2.0">
</head>
<body data-deck-id="kr-flow-demo" data-course="Knowledge Representation" data-session="Design system" data-duration="6" data-app-root="../" data-unit="Lebanese University · MSc">
<div class="deck">
<div class="deck__stage">
'''
TAIL = '''
</div>
</div>
<script src="../assets/lu-deck.js?v=1.1.0" defer></script>
<script src="../assets/lu-flow.js?v=1.2.0" defer></script>
</body>
</html>
'''
S = []
S.append('''<section class="slide" data-label="Colour is meaning" data-section="Flow diagrams" data-minutes="2">
  <div class="lu-eyebrow">Design system v1.2 · flow diagrams</div>
  <h2 class="lu-h2">In every diagram, a colour tells you where a class comes from.</h2>
  <div class="lu-split lu-split--wide-left">
    <table class="lu-table">
      <thead><tr><th>Colour</th><th>Means</th><th>Example</th></tr></thead>
      <tbody>
        <tr><td><b style="color:var(--lu-blue-700)">Blue</b></td><td>Our own ontology</td><td><code>ul:</code> Order for a sole-sourced good</td></tr>
        <tr><td><b style="color:var(--lu-teal-700)">Teal</b></td><td>A domain ontology we reuse</td><td><code>ioc:</code> SupplyRelationship</td></tr>
        <tr><td><b style="color:var(--lu-plum-700)">Plum</b></td><td>BFO, the upper ontology</td><td>independent continuant</td></tr>
        <tr><td><b style="color:var(--lu-green-700)">Green pill</b></td><td>One individual thing</td><td>shipment 4473</td></tr>
        <tr><td><b style="color:var(--lu-amber-700)">Amber, dashed</b></td><td>Inferred by the reasoner</td><td>the badge says <i>inferred</i></td></tr>
        <tr><td><b style="color:var(--lu-red-700)">Red</b></td><td>Impossible, an error</td><td>equivalent to owl:Nothing</td></tr>
      </tbody>
    </table>
    <div class="lu-stack">
      <div class="lu-callout lu-callout--concept"><span class="lu-callout__label">Why these, and why this order</span>
        <p class="lu-sub">Blue, teal, plum follow the <b>reuse stack</b> from Session 3: ours on top, then the domain ontology, then BFO. Amber matches the <b>yellow</b> Protégé uses for inferred facts, and red matches its red for impossible classes, so the slide and the tool speak the same language.</p></div>
      <p class="lu-sub">A state never hides the layer: an inferred teal class stays teal, with an amber dashed outline. Only <b>impossible</b> overrides, because an error must win the eye.</p>
    </div>
  </div>
  <template data-notes><p>Design system reference slide, not course material.</p></template>
</section>''')
S.append(f'''<section class="slide" data-label="The reasoner's proof, step by step" data-section="Flow diagrams" data-minutes="3">
  <div class="lu-eyebrow">Session 3 · reading an explanation</div>
  <h2 class="lu-h2">Why is &ldquo;Order for a sole-sourced good&rdquo; impossible?</h2>
  <div class="lu-walk" data-label="Why the order class is impossible">
      <div class="lu-walk__view">
        <div class="lu-flow"><script type="application/json" class="lu-flow__spec">{spec}</script></div>
{steps}
      </div>
    </div>
  <template data-notes><p>Click the diagram, then use the arrow keys or Next step. The amber dots are the reasoner's attention; they turn red on a conflict.</p></template>
</section>''')
S.append('''<section class="slide" data-label="How to write one" data-section="Flow diagrams" data-minutes="1">
  <div class="lu-eyebrow">For authors</div>
  <h2 class="lu-h2">Write the blocks, arrows and steps. The component draws them.</h2>
  <div class="lu-split">
    <div class="lu-code lu-code--sm" data-name="the spec, shortened"><pre><code>{ "width": 1448, "height": 358,
  "nodes": [
    { "id": "order", "label": "Order for a\\nsole-sourced good",
      "kind": "ours", "x": 125, "y": 160, "w": 230, "h": 86 }
  ],
  "edges": [
    { "id": "e2", "from": "product", "to": "supply",
      "label": "domain", "kind": "inferred" }
  ],
  "steps": [
    { "show": ["supply", "e2"], "run": ["e2"],
      "set": { "supply": "inferred" } }
  ]
}</code></pre></div>
    <ul class="lu-list">
      <li>Arrows name their two blocks, so they <b>always touch them</b>, however the blocks move.</li>
      <li><code>kind</code> picks the colour from the design system. No hex values in a lecture, ever.</li>
      <li>Steps follow the walkthrough bar: arrow keys, dots, <b>Next step</b>.</li>
    </ul>
  </div>
  <template data-notes><p>The legend is built automatically from the kinds and states used. Full reference: design-system.html, section 7.</p></template>
</section>''')
open('/tmp/kr-s4-check/lectures/proto-diagrams.html','w').write(HEAD + "\n".join(S) + TAIL)
print('built')
