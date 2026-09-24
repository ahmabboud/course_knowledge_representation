"""Shared slide builders for the Session 3 deck (course authoring standard, AGENTS.md 2c)."""


def slide(label, section, minutes, body, notes, kind="", extra_attr=""):
    cls = "slide" + (f" slide--{kind}" if kind else "")
    return (f'<section class="{cls}" data-label="{label}" data-section="{section}" '
            f'data-minutes="{minutes}"{extra_attr}>\n{body}\n'
            f'  <template data-notes>{notes}</template>\n</section>\n')


def divider(label, section, eyebrow, question, lead, notes="<p>Ten seconds. Read the question, let it hang, move on.</p>"):
    body = (f'  <div class="slide__body lu-center" style="gap:var(--lu-s5)">\n'
            f'    <div class="lu-eyebrow">{eyebrow}</div>\n'
            f'    <h2 class="lu-display-xl" style="max-width:26ch">{question}</h2>\n'
            f'    <p class="lu-lead" style="max-width:46ch">{lead}</p>\n  </div>')
    return (f'<section class="slide slide--night" data-chrome="none" data-label="{label}" '
            f'data-section="{section}" data-minutes="1">\n{body}\n'
            f'  <template data-notes>{notes}</template>\n</section>\n')


def defbox(pairs, label="Defined on this slide", build=None):
    b = f' data-build="{build}"' if build else ""
    rows = "".join(f'<dt>{t}</dt><dd>{d}</dd>' for t, d in pairs)
    return (f'<div class="lu-callout lu-callout--concept"{b}>'
            f'<span class="lu-callout__label">{label}</span>'
            f'<dl class="lu-defs">{rows}</dl></div>')


def callout(label, text, kind="", build=None):
    k = f" lu-callout--{kind}" if kind else ""
    b = f' data-build="{build}"' if build else ""
    return (f'<div class="lu-callout{k}"{b}><span class="lu-callout__label">{label}</span>'
            f'<p class="lu-sub">{text}</p></div>')


def figure(src, alt, caption, frame_ratio=None, build=None):
    b = f' data-build="{build}"' if build else ""
    style = f' style="aspect-ratio:{frame_ratio};flex:0 0 auto"' if frame_ratio else ""
    return (f'<figure class="lu-figure"{b} style="margin:0">'
            f'<div class="lu-figure__frame"{style}><img src="{src}" alt="{alt}" loading="lazy"></div>'
            f'<figcaption>{caption}</figcaption></figure>')


def placeholder(title, note, caption):
    return (f'<figure class="lu-figure" style="margin:0"><div class="lu-figure__ph">'
            f'<span class="lu-figure__ph-title">{title}</span>'
            f'<span class="lu-figure__ph-note">{note}</span></div>'
            f'<figcaption>{caption}</figcaption></figure>')


def code(name, lines_html, small=True):
    sm = " lu-code--sm" if small else ""
    return f'<div class="lu-code{sm}" data-name="{name}"><pre><code>{lines_html}</code></pre></div>'
