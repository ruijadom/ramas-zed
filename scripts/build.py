#!/usr/bin/env python3
"""
Ramas — Zed theme generator.

Ramas is a Zed port of the open-source Material Theme (Apache-2.0).
Every colour comes from ../palettes/material.json, which is extracted
verbatim from the Material Theme source (see its "_source" block).
The UI and syntax derivation below follows Material's own
`scripts/generator/color-set.ts`, translated to Zed's theme keys and
tree-sitter captures. Where Zed needs a value Material doesn't define
(e.g. a hover fill), it is derived from the same palette and marked
"zed-adapt".

Usage:
    python3 scripts/build.py                     # all variants, teal accent
    python3 scripts/build.py --accent Sky        # Material accent preset
    python3 scripts/build.py --accent "#FF9800"  # any hex
"""
import argparse
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PALETTES = os.path.join(ROOT, "palettes", "material.json")
OUT = os.path.join(ROOT, "themes", "ramas.json")

# Material variant id -> Ramas theme name. Darker HC is the flagship.
NAMES = {
    "darker-hc": "Ramas",
    "darker": "Ramas Darker",
    "default": "Ramas Default",
    "default-hc": "Ramas Default HC",
    "ocean": "Ramas Ocean",
    "ocean-hc": "Ramas Ocean HC",
    "palenight": "Ramas Palenight",
    "palenight-hc": "Ramas Palenight HC",
    "deepforest": "Ramas Deepforest",
    "deepforest-hc": "Ramas Deepforest HC",
    "lighter": "Ramas Lighter",
    "lighter-hc": "Ramas Lighter HC",
}


def al(color: str, alpha: str) -> str:
    """Set a 2-hex-digit alpha on a #RRGGBB or #RRGGBBAA colour."""
    return color[:7] + alpha


def norm(color: str) -> str:
    return color.upper()


def tok(color, style=None, weight=None):
    return {"color": norm(color), "font_style": style, "font_weight": weight}


def build_variant(name: str, appearance: str, s: dict, accent: str) -> dict:
    b = s["base"]
    fg = s["foreground"]
    bg = s["background"]
    alt = s["backgroundAlt"]
    side_fg = s["sidebarForeground"]
    comments = s["comments"]
    IT = "italic"

    style = {
        "accents": [accent, b["purple"], b["blue"], b["yellow"], b["cyan"], b["pink"], b["green"]],

        # surfaces (sideBar/panel/titleBar/statusBar/editorWidget = backgroundAlt)
        "background": alt,
        "surface.background": alt,
        "elevated_surface.background": alt,
        "panel.background": alt,
        "title_bar.background": alt,
        "title_bar.inactive_background": alt,
        "status_bar.background": alt,
        "editor.background": bg,
        "editor.gutter.background": bg,
        "editor.subheader.background": alt,
        "toolbar.background": bg,                         # breadcrumb.background
        "tab_bar.background": bg,                         # editorGroupHeader.tabsBackground
        "tab.active_background": bg,
        "tab.inactive_background": bg,
        "terminal.background": alt,                       # panel.background
        "terminal.ansi.background": alt,
        "drop_target.background": al(accent, "30"),       # zed-adapt

        # borders (sideBar/panel/titleBar/statusBar.border = contrastBorder 60)
        "border": al(s["contrastBorder"], "60"),
        "border.variant": al(s["contrastBorder"], "60"),
        "border.focused": al(accent, "50"),               # zed-adapt (sash.hoverBorder)
        "border.selected": accent,
        "border.transparent": "#00000000",
        "border.disabled": s["inputBorder"],
        "pane.focused_border": "#00000000",               # focusBorder alpha 00
        "pane_group.border": s["shadow"],                 # editorGroup.border
        "panel.focused_border": "#00000000",

        # elements
        "element.background": s["inputBackground"],      # input.background
        "element.hover": al(fg, "10"),                   # zed-adapt
        "element.active": al(accent, "30"),              # zed-adapt
        "element.selected": al(fg, "20"),                # list.focusBackground
        "element.disabled": s["inputBackground"],
        "ghost_element.background": "#00000000",
        "ghost_element.hover": al(fg, "10"),             # zed-adapt
        "ghost_element.active": al(accent, "30"),        # zed-adapt
        "ghost_element.selected": al(fg, "20"),          # list.focusBackground
        "ghost_element.disabled": "#00000000",

        # text & icons
        "text": fg,
        "text.muted": side_fg,                           # sideBar.foreground
        "text.placeholder": al(fg, "60"),                # input.placeholderForeground
        "text.disabled": comments,
        "text.accent": accent,                           # list.highlightForeground
        "icon": fg,
        "icon.muted": side_fg,
        "icon.disabled": comments,
        "icon.placeholder": side_fg,
        "icon.accent": accent,
        "link_text.hover": accent,                       # textLink.foreground

        # scrollbar
        "scrollbar.thumb.background": s["scrollbars"],
        "scrollbar.thumb.hover_background": al(accent, "80"),  # scrollbarSlider.activeBackground (alpha 50%)
        "scrollbar.thumb.border": "#00000000",
        "scrollbar.track.background": "#00000000",
        "scrollbar.track.border": "#00000000",

        # editor
        "editor.foreground": fg,
        "editor.active_line.background": al(s["lineHighlight"], "50"),
        "editor.highlighted_line.background": al(s["lineHighlight"], "50"),
        "editor.line_number": s["lineNumbers"],
        "editor.active_line_number": side_fg,            # editorLineNumber.activeForeground
        "editor.invisible": s["guides"],                 # ui.invisibles
        "editor.wrap_guide": s["guides"],                # editorRuler.foreground
        "editor.active_wrap_guide": s["guides"],
        "editor.indent_guide": al(s["guides"], "70"),    # editorIndentGuide.background
        "editor.indent_guide_active": s["guides"],       # editorIndentGuide.activeBackground
        "editor.document_highlight.read_background": al(b["pink"], "30"),    # wordHighlight
        "editor.document_highlight.write_background": al(b["green"], "30"),  # wordHighlightStrong
        "editor.document_highlight.bracket_background": al(s["caret"], "30"), # zed-adapt (bracket border caret 50)
        "panel.indent_guide": s["guides"],               # tree.indentGuidesStroke
        "panel.indent_guide_active": side_fg,
        "panel.indent_guide_hover": side_fg,
        "search.match_background": al(b["yellow"], "30"),  # findRangeHighlight

        # terminal (Material terminal palette)
        "terminal.foreground": fg,
        "terminal.bright_foreground": b["white"] if appearance == "dark" else b["black"],
        "terminal.dim_foreground": side_fg,
        "terminal.ansi.black": b["black"],
        "terminal.ansi.red": b["red"],
        "terminal.ansi.green": b["green"],
        "terminal.ansi.yellow": b["yellow"],
        "terminal.ansi.blue": b["blue"],
        "terminal.ansi.magenta": b["purple"],
        "terminal.ansi.cyan": b["cyan"],
        "terminal.ansi.white": b["white"],
        "terminal.ansi.bright_black": comments,
        "terminal.ansi.bright_red": b["red"],
        "terminal.ansi.bright_green": b["green"],
        "terminal.ansi.bright_yellow": b["yellow"],
        "terminal.ansi.bright_blue": b["blue"],
        "terminal.ansi.bright_magenta": b["purple"],
        "terminal.ansi.bright_cyan": b["cyan"],
        "terminal.ansi.bright_white": b["white"],
        "terminal.ansi.dim_black": b["black"],
        "terminal.ansi.dim_red": al(b["red"], "B3"),
        "terminal.ansi.dim_green": al(b["green"], "B3"),
        "terminal.ansi.dim_yellow": al(b["yellow"], "B3"),
        "terminal.ansi.dim_blue": al(b["blue"], "B3"),
        "terminal.ansi.dim_magenta": al(b["purple"], "B3"),
        "terminal.ansi.dim_cyan": al(b["cyan"], "B3"),
        "terminal.ansi.dim_white": side_fg,
    }

    # diagnostics & git (editorError/Warning/Info, gitDecoration.*, editorGutter.*)
    for key, color in {
        "error": b["red"],
        "warning": b["yellow"],
        "info": b["blue"],
        "hint": side_fg,
        "success": b["green"],
        "created": b["green"],
        "modified": b["blue"],
        "deleted": b["red"],
        "renamed": b["cyan"],
        "conflict": b["yellow"],
        "ignored": al(side_fg, "90"),
        "predictive": comments,
        "hidden": comments,
        "unreachable": comments,
    }.items():
        style[key] = color
        style[key + ".background"] = al(color, "20")   # diffEditor.*TextBackground uses 20
        style[key + ".border"] = al(color, "60")       # editorGutter.* uses 60

    style["players"] = [{"cursor": s["caret"], "background": s["caret"], "selection": s["selection"]}] + [
        {"cursor": c, "background": c, "selection": al(c, "30")}
        for c in (b["blue"], b["purple"], b["green"], b["orange"], b["red"], b["cyan"], b["yellow"])
    ]

    # syntax: Material tokenColors -> Zed captures (TS/TSX/JS/JSON queries)
    style["syntax"] = {
        # keywords
        "keyword": tok(b["purple"]),                     # storage.modifier: async static public extends
        "keyword.declaration": tok(b["purple"]),         # storage.type: const let function class type
        "keyword.control": tok(b["cyan"], IT),           # keyword.control
        "keyword.import": tok(b["cyan"], IT),            # keyword.control.import / export
        "keyword.operator": tok(b["cyan"]),
        "operator": tok(b["cyan"]),                      # keyword.operator
        # functions
        "function": tok(b["blue"]),                      # entity.name.function
        "function.method": tok(b["blue"]),
        "function.builtin": tok(b["blue"]),              # support.function
        "constructor": tok(b["purple"]),                 # TS `constructor` is storage.type
        # types
        "type": tok(b["yellow"]),
        "type.builtin": tok(b["yellow"]),                # support.type
        "type.class": tok(b["yellow"]),                  # entity.name.type.class
        "type.name": tok(b["yellow"]),
        "enum": tok(b["yellow"]),
        "variant": tok(b["yellow"]),
        # variables
        "variable": tok(fg),
        "variable.parameter": tok(fg, IT),               # variable.parameter → italic
        "variable.special": tok(b["cyan"]),              # variable.language.this
        "property": tok(fg),                             # variable.other.property
        "property.name": tok(b["red"]),                  # meta.object-literal.key
        "property.json_key": tok(b["purple"]),           # JSON Key - Level 0
        "constant": tok(fg),                             # variable.other.constant
        "constant.builtin": tok(b["cyan"]),              # constant.language
        "label": tok(fg),
        # literals
        "string": tok(b["green"]),
        "string.escape": tok(fg),                        # constant.character.escape
        "string.regex": tok(b["green"]),
        "string.special": tok(fg),                       # html entities
        "string.special.symbol": tok(b["cyan"]),         # constant.other.symbol
        "number": tok(b["orange"]),                      # constant.numeric
        "boolean": tok(b["pink"]),                       # constant.language.boolean
        "text.literal": tok(b["green"]),                 # markup.inline.raw
        # punctuation
        "punctuation": tok(b["cyan"]),
        "punctuation.bracket": tok(b["cyan"]),
        "punctuation.delimiter": tok(b["cyan"]),
        "punctuation.special": tok(b["cyan"]),           # template expression begin/end
        "punctuation.list_marker": tok(b["cyan"]),
        "embedded": tok(fg),                             # meta.template.expression reset
        # JSX / HTML
        "tag": tok(b["red"]),                            # entity.name.tag
        "tag.jsx": tok(b["red"]),
        "tag.component": tok(b["yellow"]),               # support.class.component
        "tag.component.jsx": tok(b["yellow"]),
        "attribute": tok(b["purple"]),                   # entity.other.attribute-name
        "attribute.jsx": tok(b["purple"]),
        "punctuation.bracket.jsx": tok(b["cyan"]),       # punctuation.definition.tag
        "punctuation.delimiter.jsx": tok(b["cyan"]),
        "text.jsx": tok(fg),                             # meta.jsx.children
        # comments & misc
        "comment": tok(comments, IT),
        "comment.doc": tok(comments, IT),
        "preproc": tok(comments),
        "hint": tok(comments, IT),
        "predictive": tok(comments, IT),
        "primary": tok(fg),
        # markdown
        "title": tok(b["cyan"]),                         # markup.heading
        "emphasis": tok(b["red"], IT),                   # markup.italic
        "emphasis.strong": tok(b["red"], None, 700),     # markup.bold
        "link_text": tok(b["red"]),                      # meta.link.inline
        "link_uri": tok(b["red"]),
    }

    # normalise case
    for k, v in list(style.items()):
        if isinstance(v, str):
            style[k] = norm(v)
    style["accents"] = [norm(c) for c in style["accents"]]
    style["players"] = [{k: norm(v) for k, v in p.items()} for p in style["players"]]

    return {"name": name, "appearance": appearance, "style": style}


def main():
    data = json.load(open(PALETTES))
    accents = {k.lower().replace(" ", "-"): v for k, v in data["accents"].items()}

    ap = argparse.ArgumentParser()
    ap.add_argument("--accent", default="teal",
                    help="Material accent preset (" + ", ".join(sorted(accents)) + ") or #RRGGBB")
    ap.add_argument("--out", default=OUT)
    args = ap.parse_args()

    key = args.accent.lower().replace(" ", "-")
    accent = accents.get(key, args.accent)
    if not (accent.startswith("#") and len(accent) == 7):
        raise SystemExit(f"invalid accent: {args.accent}")

    themes = [
        build_variant(NAMES[vid], v["type"], v["scheme"], accent)
        for vid, v in data["variants"].items()
    ]
    family = {
        "$schema": "https://zed.dev/schema/themes/v0.2.0.json",
        "name": "Ramas",
        "author": "Rui",
        "themes": themes,
    }
    out = os.path.expanduser(args.out)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w") as f:
        json.dump(family, f, indent=2)
        f.write("\n")
    print(f"wrote {out}: {len(themes)} themes, accent {accent}")


if __name__ == "__main__":
    main()
