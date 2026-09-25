"""Tiny SVG helpers for the Session 3 deck.

Every diagram is drawn in a viewBox equal to the width it renders at on the
1600x900 slide canvas, so the design system's 22px / 20px SVG text renders at
true size (never below 20px). Arrowheads are drawn as polygons, not markers:
markers defined inside a hidden slide or walkthrough step do not render.
Colours come only from existing --lu-* tokens, with the meaning lu-flow gives
them (AGENTS.md section 7, route 0): blue is our ontology, green an
individual, amber something the reasoner inferred, red only something
impossible or refused. Never pick a colour for looks.
"""
import math
from html import escape

FULL = 1448   # content width of a slide
HALF = 688    # one column of .lu-split
WL = 803      # wide column of .lu-split--wide-left / --wide-right
NL = 573      # narrow column

INK = "var(--lu-ink)"
INK2 = "var(--lu-ink-2)"
INK3 = "var(--lu-ink-3)"
RED = "var(--lu-red-700)"
RED_BG = "var(--lu-red-050)"
RED_BG2 = "var(--lu-red-100)"
GREEN = "var(--lu-green-700)"
GREEN_BG = "var(--lu-green-050)"
GREEN_BG2 = "var(--lu-green-100)"
PAPER2 = "var(--lu-paper-2)"
LINE = "var(--lu-line-2)"
BLUE = "var(--lu-blue-700)"
BLUE_BG = "var(--lu-blue-050)"
BLUE_TXT = "var(--lu-blue-900)"
AMBER = "var(--lu-amber-700)"
TEAL = "var(--lu-teal-700)"
TEAL_BG = "var(--lu-teal-050)"


def svg(w, h, body, label):
    return (f'<svg class="lu-svg" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(label)}">'
            f'<title>{escape(label)}</title>{body}</svg>')


def text(x, y, s, cls="", anchor="middle", color=None, weight=None, italic=False):
    attrs = [f'x="{x}"', f'y="{y}"', f'text-anchor="{anchor}"', 'dominant-baseline="middle"']
    if cls:
        attrs.append(f'class="{cls}"')
    style = []
    if color:
        style.append(f"fill:{color}")
    if weight:
        style.append(f"font-weight:{weight}")
    if italic:
        style.append("font-style:italic")
    if style:
        attrs.append(f'style="{";".join(style)}"')
    return f'<text {" ".join(attrs)}>{s}</text>'


def box(cx, cy, w, h, label, kind="class", sub=None):
    """A node. kind: class (blue, our ontology), ind (green pill), lit (grey mono),
    note (dashed grey), bad (red fill: impossible), muted, plain."""
    rx = {"class": 8, "ind": h / 2, "lit": 6, "note": 6, "bad": 8, "muted": 8, "plain": 8}[kind]
    fill, stroke, dash, tcol = {
        "class": (BLUE_BG, BLUE, None, BLUE_TXT),
        "ind": (GREEN_BG, GREEN, None, "var(--lu-green-900)"),
        "lit": (PAPER2, INK3, None, INK),
        "note": ("var(--lu-paper)", INK3, "6 5", INK2),
        "bad": (RED_BG2, RED, None, "var(--lu-red-900)"),
        "muted": ("var(--lu-paper)", LINE, None, INK3),
        "plain": ("var(--lu-paper)", INK2, None, INK),
    }[kind]
    d = f' stroke-dasharray="{dash}"' if dash else ""
    out = (f'<rect x="{cx - w / 2}" y="{cy - h / 2}" width="{w}" height="{h}" rx="{rx}" '
           f'style="fill:{fill};stroke:{stroke};stroke-width:2"{d}/>')
    cls = "s-mono" if kind == "lit" else ""
    if sub:
        out += text(cx, cy - 13, label, cls, color=tcol, weight=600)
        out += text(cx, cy + 15, sub, "s-label", color=INK3)
    else:
        out += text(cx, cy, label, cls, color=tcol, weight=600 if kind != "note" else None)
    return out


def arrow(x1, y1, x2, y2, label=None, kind="strong", lx=None, ly=None, both=False, label_anchor="middle"):
    """Line with a polygon head at (x2, y2). kind: strong, infer (dashed amber), red, muted."""
    col = {"strong": INK2, "infer": AMBER, "red": RED, "muted": LINE, "green": GREEN}[kind]
    dash = ' stroke-dasharray="8 6"' if kind == "infer" else ""
    out = f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" style="stroke:{col};stroke-width:2.5"{dash}/>'

    def head(xa, ya, xb, yb):
        ang = math.atan2(yb - ya, xb - xa)
        L, W = 14, 7
        p1 = (xb, yb)
        p2 = (xb - L * math.cos(ang) + W * math.sin(ang), yb - L * math.sin(ang) - W * math.cos(ang))
        p3 = (xb - L * math.cos(ang) - W * math.sin(ang), yb - L * math.sin(ang) + W * math.cos(ang))
        return f'<polygon points="{p1[0]:.1f},{p1[1]:.1f} {p2[0]:.1f},{p2[1]:.1f} {p3[0]:.1f},{p3[1]:.1f}" style="fill:{col}"/>'

    out += head(x1, y1, x2, y2)
    if both:
        out += head(x2, y2, x1, y1)
    if label:
        mx = lx if lx is not None else (x1 + x2) / 2
        my = ly if ly is not None else (y1 + y2) / 2 - 16
        out += text(mx, my, label, "s-mono", anchor=label_anchor, color=col if kind != "strong" else INK2)
    return out


def circle(cx, cy, r, label=None, color="red", lx=None, ly=None, fill=True, dashed=False, anchor="middle"):
    stroke, bg = {"ours": (BLUE, BLUE_BG), "reused": (TEAL, TEAL_BG), "red": (RED, RED_BG), "green": (GREEN, GREEN_BG), "ink": (INK2, PAPER2),
                  "muted": (LINE, "var(--lu-paper)")}[color]
    f = bg if fill else "none"
    d = ' stroke-dasharray="8 6"' if dashed else ""
    out = f'<circle cx="{cx}" cy="{cy}" r="{r}" style="fill:{f};stroke:{stroke};stroke-width:2"{d}/>'
    if label:
        out += text(lx if lx is not None else cx, ly if ly is not None else cy - r + 26, label,
                    anchor=anchor, color=stroke, weight=600)
    return out


def dot(cx, cy, label=None, color="green", lx=None, ly=None, anchor="start"):
    col = {"green": GREEN, "red": RED, "ink": INK2, "ours": BLUE, "reused": TEAL}[color]
    out = f'<circle cx="{cx}" cy="{cy}" r="9" style="fill:{col}"/>'
    if label:
        out += text(lx if lx is not None else cx + 16, ly if ly is not None else cy, label,
                    "s-label", anchor=anchor, color=INK2)
    return out


def line(x1, y1, x2, y2, color=LINE, width=2, dashed=False):
    d = ' stroke-dasharray="8 6"' if dashed else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" style="stroke:{color};stroke-width:{width}"{d}/>'


def rect(x, y, w, h, fill="var(--lu-paper)", stroke=LINE, rx=10, dashed=False, width=2):
    d = ' stroke-dasharray="8 6"' if dashed else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" style="fill:{fill};stroke:{stroke};stroke-width:{width}"{d}/>'


def tick(x, y, ok=True):
    col = GREEN if ok else RED
    if ok:
        return f'<path d="M {x-9} {y} L {x-2} {y+8} L {x+11} {y-9}" style="stroke:{col};stroke-width:4;fill:none"/>'
    return (f'<path d="M {x-9} {y-9} L {x+9} {y+9} M {x+9} {y-9} L {x-9} {y+9}" '
            f'style="stroke:{col};stroke-width:4;fill:none"/>')
