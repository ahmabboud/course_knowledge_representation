"""Standalone Protege guide deck, part 1. Every screenshot is real, captured 2026-09-22."""
from common import slide, divider, defbox, callout

IMG = "../assets/img/"
SLIDES = []


def shot(name, alt, caption, height=420, width="100%", border=True):
    b = ";border:1px solid var(--lu-line-2)" if border else ""
    return (f'<figure class="lu-figure" style="margin:0;min-height:0">'
            f'<div class="lu-figure__frame" style="flex:0 0 auto;height:{height}px;width:{width};'
            f'background:var(--lu-paper-2){b}">'
            f'<img src="{IMG}{name}" alt="{alt}" loading="lazy" style="object-fit:contain">'
            f'</div><figcaption>{caption}</figcaption></figure>')


# ------------------------------------------------------------------ 01 Title
SLIDES.append('''<section class="slide slide--night" data-chrome="none" data-label="Title" data-section="Getting ready" data-minutes="1">
  <div class="slide__body" style="justify-content:space-between">
    <div class="lu-row" style="justify-content:space-between;align-items:flex-start">
      <div class="lu-lockup">
        <span class="lu-lockup__mark">LU</span>
        <span class="lu-lockup__text">
          <span class="lu-lockup__name">Lebanese University</span>
          <span class="lu-lockup__unit">Faculty of Sciences &middot; MSc Computer Science</span>
        </span>
      </div>
      <div class="lu-tag lu-tag--red" style="background:transparent;color:#FF9AA7;border-color:#96122B">Tool guide &middot; read before Session 3</div>
    </div>
    <div class="lu-stack">
      <div class="lu-eyebrow">Knowledge Representation &middot; Protégé 5.6</div>
      <h1 class="lu-display" style="max-width:24ch">Protégé, one screen at a time</h1>
      <p class="lu-lead" style="max-width:48ch">Every screen below is a real screenshot of our own supply chain ontology, taken while writing this guide. Follow it once, before the session, and the lab will feel like a repeat.</p>
    </div>
    <div class="lu-row" style="justify-content:space-between;font-size:var(--lu-t-caption);color:var(--lu-on-night-2)">
      <span>About 40 minutes at your own pace &middot; 23 screens</span>
      <span>Press <kbd>&rarr;</kbd> to begin &middot; <kbd>?</kbd> for shortcuts</span>
    </div>
  </div>
  <template data-notes><p>This guide exists because Session 3 assumes the tool. Rule in AGENTS.md section 2c: no tool before its guide.</p></template>
</section>
''')

# ------------------------------------------------------------------ 02 What it is
SLIDES.append(slide("What Protégé is", "Getting ready", 2, '''  <div class="lu-eyebrow">Orientation</div>
  <h2 class="lu-h2">Protégé is a text editor for meaning, with a calculator attached</h2>
  <div class="lu-split lu-split--wide-left">
    <div class="lu-stack">
      <p class="lu-p">You type facts about <b>classes</b> (kinds of thing) and <b>individuals</b> (single things). You never type the conclusions. A separate program, the <b>reasoner</b>, computes those on demand and shows them in a different colour.</p>
      <table class="lu-table">
        <thead><tr><th>Thing</th><th>What it is</th><th>Where it lives</th></tr></thead>
        <tbody>
          <tr><td><b>The editor</b></td><td>Protégé 5.6, a desktop application</td><td>Applications folder</td></tr>
          <tr><td><b>The ontology file</b></td><td>Plain text, Turtle syntax, <code>.ttl</code></td><td><code>demos/session-03-ontology/workspace/</code></td></tr>
          <tr><td><b>The reasoner</b></td><td>ELK or HermiT, shipped inside Protégé</td><td>The Reasoner menu</td></tr>
        </tbody>
      </table>
      <p class="lu-sub">Prefer video first? The instructor recommends this short series on Protégé fundamentals: <a href="https://www.youtube.com/watch?v=CduRWyyL3q8&amp;list=PLNohRKRAHaszTV3puqFM9yXDXnEqjS6Fd" target="_blank" rel="noopener">YouTube, The AI &amp; DS Channel</a>. Then come back here: this guide uses our exact files.</p>
    </div>
    <div class="lu-stack">
      ''' + defbox([("ontology", "A file that says what the words of a domain mean, precisely enough for a program to draw conclusions."),
                    ("reasoner", "A program that reads those meanings and computes what follows from them."),
                    ("Protégé", "The editor we use to write and inspect the file, and to run the reasoner over it.")]) + '''
      ''' + callout("Protégé is not a database", "It holds one ontology in memory and forgets everything when you quit. Nothing you do here touches DataCo or the graph from Session 2 unless you save the file yourself.", "neutral") + '''
    </div>
  </div>''', '''<p>Students who have used Protégé before still read this page: the asserted versus inferred distinction is the one thing everybody gets wrong.</p>'''))

# ------------------------------------------------------------------ 03 Before you start
SLIDES.append(slide("Before you open anything", "Getting ready", 2, '''  <div class="lu-eyebrow">Setup, once</div>
  <h2 class="lu-h2">One command builds the folder you will open files from</h2>
  <div class="lu-split">
    <div class="lu-stack">
      <div class="lu-code lu-code--sm" data-name="terminal"><pre><code>cd demos/session-03-ontology
python3 fetch_ontologies.py</code></pre></div>
      <p class="lu-sub">It downloads BFO and the IOF supply chain ontology once, copies our three course files next to them, and writes a catalog so Protégé can find every import offline.</p>
      ''' + callout("Check it worked", "The folder <code>workspace/</code> now holds <code>catalog-v001.xml</code> and five <code>.ttl</code> files. If it does not, run the command again and read the last line it prints.", "neutral") + '''
    </div>
    <div class="lu-stack">
      <table class="lu-table">
        <thead><tr><th>File in workspace</th><th>What you do with it</th></tr></thead>
        <tbody>
          <tr><td><code>scro-extension-v0.ttl</code></td><td>The starting point. It contains a real modelling error, on purpose.</td></tr>
          <tr><td><code>scro-extension-reference.ttl</code></td><td>The fixed version. Open it only after you have found the error yourself.</td></tr>
          <tr><td><code>sample-shipments.ttl</code></td><td>Three shipments and two carriers, for the last step.</td></tr>
          <tr><td><code>catalog-v001.xml</code></td><td>Never opened by hand. Protégé reads it to resolve imports.</td></tr>
        </tbody>
      </table>
      ''' + defbox([("catalog file", "A small XML file that maps an ontology address on the web to a copy on your disk, so imports load with no internet.")]) + '''
    </div>
  </div>''', '''<p>The catalog is the single most common cause of "it will not load" on a university network. Say so out loud.</p>'''))

# ------------------------------------------------------------------ 04 Open
SLIDES.append(slide("Step 1, open the file", "Getting ready", 2, '''  <div class="lu-eyebrow">Step 1 of 12</div>
  <h2 class="lu-h2">File, then Open, then <code>workspace/scro-extension-v0.ttl</code></h2>
  <div class="lu-split lu-split--wide-right">
    <div class="lu-stack">
      <ol class="lu-list lu-list--num">
        <li>Start Protégé and wait for the empty window.</li>
        <li>Menu <b>File &rsaquo; Open...</b> and pick the file inside <code>workspace/</code>, not the one in the folder above it.</li>
        <li>Protégé asks whether to reuse the window you are in. Either answer works: <b>No</b> keeps the empty window and opens a second one.</li>
        <li>Loading takes a few seconds. BFO and the supply chain ontology load with it.</li>
      </ol>
      ''' + callout("Open the file in workspace/", "The copies in <code>demos/session-03-ontology/</code> have no catalog next to them, so their imports will not resolve.", "neutral") + '''
    </div>
    ''' + shot("s3-protege-01-open-in-current-window.png",
               "Protege dialog asking whether to open the ontology in the current window, with Cancel, No and Yes buttons.",
               "The prompt you get on <b>File &rsaquo; Open</b>. <b>No</b> opens a second window, which is handy when you want to compare two files.", 150, "500px") + '''
  </div>''', '''<p>If a student opens the wrong copy, the class tree shows only a handful of classes and no BFO. That is the tell.</p>'''))

# ------------------------------------------------------------------ 05 Window map
SLIDES.append(slide("Step 2, the window map", "The window", 3, '''  <div class="lu-eyebrow">Step 2 of 12</div>
  <h2 class="lu-h2">Five places on this screen, and nothing else matters today</h2>
  ''' + shot("s3-protege-04-class-primitive.png",
             "The Protege window with the Entities tab open, the class tree on the left and the description of the selected class on the right.",
             "The <b>Entities</b> tab with a class selected. Left, the tree of classes. Right, everything said about the one you clicked.", 440) + '''
  <div class="lu-cards" style="grid-template-columns:repeat(5,minmax(0,1fr))">
    <div class="lu-card lu-card--flat"><span class="lu-card__label">1 &middot; Tab bar</span><p class="lu-sub">Active ontology, Entities, Individuals by class, DL Query</p></div>
    <div class="lu-card lu-card--flat"><span class="lu-card__label">2 &middot; Class hierarchy</span><p class="lu-sub">Every class, as a tree under <code>owl:Thing</code></p></div>
    <div class="lu-card lu-card--flat"><span class="lu-card__label">3 &middot; Asserted or Inferred</span><p class="lu-sub">The dropdown above the tree. Read it before you believe the tree</p></div>
    <div class="lu-card lu-card--flat"><span class="lu-card__label">4 &middot; Annotations</span><p class="lu-sub">Labels and definitions for humans. No logic here</p></div>
    <div class="lu-card lu-card--flat"><span class="lu-card__label">5 &middot; Description</span><p class="lu-sub">The logic: Equivalent To, SubClass Of, the parts a reasoner uses</p></div>
  </div>''', '''<p>Make them find the Asserted dropdown physically with the mouse now. It is the control the whole session turns on.</p>'''))

# ------------------------------------------------------------------ 06 Tabs
SLIDES.append(slide("Which tab answers which question", "The window", 3, '''  <div class="lu-eyebrow">Orientation</div>
  <h2 class="lu-h2">Four tabs, four questions</h2>
  <table class="lu-table">
    <thead><tr><th>Tab</th><th>The question it answers</th><th>You use it for</th></tr></thead>
    <tbody>
      <tr><td><b>Active ontology</b></td><td>What did I just load, and what came with it?</td><td>Counting axioms, checking that imports resolved to local files</td></tr>
      <tr><td><b>Entities</b></td><td>What does this class or property mean?</td><td>Most of the session: reading and editing class descriptions</td></tr>
      <tr><td><b>Individuals by class</b></td><td>Which single things fall under this class?</td><td>The last step, after the reasoner has classified the data</td></tr>
      <tr><td><b>DL Query</b></td><td>Which things match a description I type right now?</td><td>Ad hoc questions, when the tab is configured in your window</td></tr>
    </tbody>
  </table>
  <div class="lu-split">
    ''' + shot("s3-protege-02-active-ontology.png",
               "Active ontology tab showing the ontology address, annotations and a metrics panel with 4,819 axioms and 254 classes.",
               "<b>Active ontology.</b> The metrics panel on the right is how you prove the imports came in: 254 classes, not the dozen we wrote.", 290) + '''
    <div class="lu-stack">
      ''' + defbox([("axiom", "One statement in the file. A label, a subclass line and a restriction are each one axiom."),
                    ("import", "A line in our file that pulls another ontology in whole, so we can reuse its classes instead of inventing our own.")]) + '''
      ''' + callout("What the numbers mean here", "Our own file is about 130 axioms. The other 4,700 arrive from BFO and the supply chain ontology we import. Reuse is most of what you are looking at.", "neutral") + '''
    </div>
  </div>''', '''<p>Ask: where did 254 classes come from when our file defines about a dozen? Answer: imports, which is Part 4 of the session.</p>'''))

# ------------------------------------------------------------------ 07 Finding things
SLIDES.append(slide("Step 3, finding anything by name", "The window", 2, '''  <div class="lu-eyebrow">Step 3 of 12</div>
  <h2 class="lu-h2">The tree is 254 classes deep. Search instead of scrolling</h2>
  <div class="lu-split lu-split--wide-left">
    <div class="lu-stack">
      <ol class="lu-list lu-list--num">
        <li>Press <kbd>cmd</kbd> <kbd>F</kbd> on macOS, <kbd>ctrl</kbd> <kbd>F</kbd> on Windows and Linux. A <b>Search</b> window opens on top.</li>
        <li>Type part of the name, for example <code>At-risk</code>. Results appear as you type, grouped by where the text was found: display name, label, or inside a logical axiom.</li>
        <li><b>Double click</b> the row whose "Found in" column says <b>Display name</b>. The tree behind the window jumps to that entity.</li>
        <li>Close the Search window. The entity stays selected underneath.</li>
      </ol>
      ''' + callout("Read the Found in column", "A hit under <b>SubClassOf</b> means the words appear inside some other class's logic, not that you found the class itself.", "neutral") + '''
    </div>
    <div class="lu-stack">
      ''' + callout("The breadcrumb is your map", "Above the tab bar, Protégé prints the path of the selected class, for example entity, continuant, independent continuant, material entity, ioc:Shipment, At-risk shipment. That line tells you where you are without scrolling the tree.", "concept") + '''
      ''' + callout("Do not trust a stale search", "The Search window keeps its last query. Select the text in the box before typing a new term, or you will be searching for the previous one.", "neutral") + '''
    </div>
  </div>''', '''<p>Demonstrate once: search At-risk, double click, close, and point at the breadcrumb.</p>'''))

# ------------------------------------------------------------------ 08 Reading a class
SLIDES.append(slide("Step 4, reading one class", "The window", 4, '''  <div class="lu-eyebrow">Step 4 of 12</div>
  <h2 class="lu-h2">Two panels: what humans read, and what the reasoner reads</h2>
  ''' + shot("s3-protege-z-a-primitive-desc.png",
             "Description panel for At-risk shipment showing an empty Equivalent To section and two SubClass Of rows: handled by some Sanctioned carrier, and ioc:Shipment.",
             "The <b>Description</b> panel of <code>At-risk shipment</code> in the starting file. <b>Equivalent To is empty</b>, and that single fact decides what the reasoner can do with this class.", 200) + '''
  <div class="lu-split">
    ''' + defbox([("SubClass Of", "A one way rule. Every at risk shipment is handled by a sanctioned carrier. Nothing says the reverse."),
                  ("Equivalent To", "A two way rule, a definition. Anything handled by a sanctioned carrier is, by that fact alone, an at risk shipment.")]) + '''
    ''' + callout("Why you care, in one line", "With SubClass Of only, the reasoner can never <b>put</b> a shipment into this class. With Equivalent To it can, and in the last step it does exactly that.", "concept") + '''
  </div>''', '''<p>This is the primitive versus defined distinction from the lecture, seen in the tool.</p>'''))

# ------------------------------------------------------------------ 09 Divider
SLIDES.append(divider("Part 2 of the guide", "The reasoner",
                      "Screens 9 to 15",
                      "Now the calculator.",
                      "Everything so far was typing. Nothing you typed has been checked yet.",
                      "<p>Pause here. Everything before this point is data entry, everything after is inference.</p>"))
