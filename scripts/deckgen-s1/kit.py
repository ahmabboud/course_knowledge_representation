"""Slide builders for the Session 1 deck (course authoring standard, AGENTS.md 2c).

Every diagram with blocks and arrows is an lu-flow spec (AGENTS.md section 7,
route 0). Session 1 has no ontology yet, so blocks keep the default grey kind
and only states carry colour: active ring, red for a broken rule, amber for
something derived. Numbers on slides come from
demos/session-01-environment-and-constraints/reference-outputs/s1-facts.txt.
"""
import html
import json


def slide(label, section, minutes, body, notes, kind="", extra=""):
    cls = "slide" + (f" slide--{kind}" if kind else "")
    return (f'<section class="{cls}" data-label="{label}" data-section="{section}" '
            f'data-minutes="{minutes}"{extra}>\n{body}\n'
            f'  <template data-notes>{notes}</template>\n</section>\n')


def divider(label, section, eyebrow, question, lead,
            notes="<p>Ten seconds. Read the question, let it hang, move on.</p>"):
    body = (f'  <div class="slide__body lu-center" style="gap:var(--lu-s5)">\n'
            f'    <div class="lu-eyebrow">{eyebrow}</div>\n'
            f'    <h2 class="lu-display-xl" style="max-width:26ch">{question}</h2>\n'
            f'    <p class="lu-lead" style="max-width:46ch">{lead}</p>\n  </div>')
    return (f'<section class="slide slide--night" data-chrome="none" data-label="{label}" '
            f'data-section="{section}" data-minutes="1">\n{body}\n'
            f'  <template data-notes>{notes}</template>\n</section>\n')


def head(eyebrow, title, size="h2", width=66):
    return (f'  <div class="lu-eyebrow">{eyebrow}</div>\n'
            f'  <h2 class="lu-{size}" style="max-width:{width}ch">{title}</h2>\n')


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


def figure(src, alt, caption, build=None):
    b = f' data-build="{build}"' if build else ""
    return (f'<figure class="lu-figure"{b} style="margin:0">'
            f'<div class="lu-figure__frame"><img src="{src}" alt="{alt}" loading="lazy"></div>'
            f'<figcaption>{caption}</figcaption></figure>')


def table(headers, rows, caption="", cls="lu-table", build=None):
    b = f' data-build="{build}"' if build else ""
    th = "".join(f"<th>{h}</th>" for h in headers)
    tr = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    cap = f"<caption>{caption}</caption>" if caption else ""
    return f'<table class="{cls}"{b}><thead><tr>{th}</tr></thead><tbody>{tr}</tbody>{cap}</table>'


def bar(value, total, text=None, tone="ink"):
    """A proportion bar for a real count. Colour is a design token, never a hex value."""
    pct = 100.0 * value / total
    colour = {"ink": "var(--lu-ink-2)", "red": "var(--lu-red-700)"}[tone]
    label = text if text is not None else f"{value:,}"
    return (f'<span class="lu-row" style="gap:var(--lu-s3);align-items:center">'
            f'<span style="flex:1;height:14px;background:var(--lu-paper-2);border-radius:7px;overflow:hidden">'
            f'<span style="display:block;height:100%;width:{pct:.1f}%;background:{colour}"></span></span>'
            f'<span class="lu-mono" style="min-width:9ch;text-align:right">{label}</span></span>')


def node(id, label, x, y, w=220, h=76, **kw):
    n = {"id": id, "label": label, "x": x, "y": y, "w": w, "h": h}
    n.update(kw)
    return n


def edge(id, a, b, label="", **kw):
    e = {"id": id, "from": a, "to": b, "label": label}
    e.update(kw)
    return e


def flow(label, width, height, nodes, edges, steps, captions=None, flags=None, legend=False):
    """An lu-flow diagram. With captions it sits in an .lu-walk and animates step by step;
    without, it is a still picture showing every step at once. legend: False, or
    {kind: label} to name the colour layers (Session 3 onward)."""
    spec = {"width": width, "height": height, "nodes": nodes, "edges": edges,
            "steps": steps, "legend": legend}
    if flags:
        spec["flags"] = flags
    js = json.dumps(spec, ensure_ascii=False)
    host = f'<div class="lu-flow"><script type="application/json" class="lu-flow__spec">{js}</script></div>'
    if not captions:
        return host
    assert len(captions) == len(steps), (label, len(captions), len(steps))
    divs = "".join(
        f'<div data-walk-step="{i}" data-caption-short="{html.escape(short, quote=True)}" '
        f'data-caption="{html.escape(cap, quote=True)}"></div>'
        for i, (short, cap) in enumerate(captions, 1))
    return (f'<div class="lu-walk" data-label="{html.escape(label, quote=True)}">'
            f'<div class="lu-walk__view">{host}{divs}</div></div>')


def defnote(pairs, label="Defined on this slide", build=None):
    """Definitions for a narrow column: one short paragraph per term, no two column grid."""
    b = f' data-build="{build}"' if build else ""
    rows = "".join(f'<p class="lu-sub"><b>{t}</b>: {d}</p>' for t, d in pairs)
    return (f'<div class="lu-callout lu-callout--concept"{b}>'
            f'<span class="lu-callout__label">{label}</span>{rows}</div>')
