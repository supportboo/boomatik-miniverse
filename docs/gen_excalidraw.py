#!/usr/bin/env python3
"""Generate the Boomatik Miniverse architecture diagram as an .excalidraw file.

Honest map of a small Vite + TypeScript pixel-art visualization that renders the
BOO agent team in a stadium and polls a local agent REST API.

Run:
    python docs/gen_excalidraw.py
Output:
    docs/boomatik-miniverse-architecture.excalidraw
"""

import json
import os
import random
import time

# ---- BOO Verse palette (violeta multicolor) ----
C1 = "#8B5CF6"  # violet
C2 = "#EC4899"  # pink
C3 = "#06B6D4"  # cyan
INK = "#1e1b2e"
FAINT = "#f5f3ff"

FONT_CODE = 3   # code font family in Excalidraw
FONT_HAND = 1   # hand-drawn

_rng = random.Random(42)


def _id(prefix="el"):
    return f"{prefix}-{_rng.randrange(16**8):08x}"


def _seed():
    return _rng.randrange(1, 2**31)


def rect(x, y, w, h, stroke=INK, bg="transparent", fill="solid",
         rounded=True, dash="solid", width=2):
    """A rectangle element."""
    return {
        "id": _id("rect"),
        "type": "rectangle",
        "x": x, "y": y, "width": w, "height": h,
        "angle": 0,
        "strokeColor": stroke,
        "backgroundColor": bg,
        "fillStyle": fill,
        "strokeWidth": width,
        "strokeStyle": dash,
        "roughness": 1,
        "opacity": 100,
        "groupIds": [],
        "frameId": None,
        "roundness": {"type": 3} if rounded else None,
        "seed": _seed(),
        "version": 1, "versionNonce": _seed(),
        "isDeleted": False,
        "boundElements": [],
        "updated": int(time.time() * 1000),
        "link": None, "locked": False,
    }


def text(x, y, content, size=16, color=INK, font=FONT_HAND, align="left", w=None):
    """A standalone text element."""
    lines = content.split("\n")
    width = w if w is not None else max(8, max(len(l) for l in lines)) * size * 0.6
    height = len(lines) * (size * 1.25)
    return {
        "id": _id("txt"),
        "type": "text",
        "x": x, "y": y, "width": width, "height": height,
        "angle": 0,
        "strokeColor": color,
        "backgroundColor": "transparent",
        "fillStyle": "solid",
        "strokeWidth": 1,
        "strokeStyle": "solid",
        "roughness": 1,
        "opacity": 100,
        "groupIds": [],
        "frameId": None,
        "roundness": None,
        "seed": _seed(),
        "version": 1, "versionNonce": _seed(),
        "isDeleted": False,
        "boundElements": [],
        "updated": int(time.time() * 1000),
        "link": None, "locked": False,
        "text": content,
        "fontSize": size,
        "fontFamily": font,
        "textAlign": align,
        "verticalAlign": "top",
        "containerId": None,
        "originalText": content,
        "lineHeight": 1.25,
        "baseline": int(size),
    }


def node(x, y, w, h, title, subtitle="", color=C1, bg=FAINT):
    """A labelled box (rectangle + title + optional subtitle). Returns list of elements
    and exposes the bounding box for arrow anchoring via the first element."""
    els = []
    box = rect(x, y, w, h, stroke=color, bg=bg, fill="solid", width=2)
    box["_box"] = (x, y, w, h)
    els.append(box)
    els.append(text(x + 12, y + 12, title, size=16, color=INK, font=FONT_CODE, w=w - 24))
    if subtitle:
        els.append(text(x + 12, y + 36, subtitle, size=11, color="#52525b",
                        font=FONT_HAND, w=w - 24))
    return els


def _center(box_el):
    x, y, w, h = box_el["_box"]
    return (x + w / 2, y + h / 2)


def arrow(src_box, dst_box, color=INK, label="", dash="solid"):
    """An arrow between two node() boxes, anchored center-to-center."""
    x1, y1 = _center(src_box)
    x2, y2 = _center(dst_box)
    els = []
    a = {
        "id": _id("arr"),
        "type": "arrow",
        "x": x1, "y": y1,
        "width": x2 - x1, "height": y2 - y1,
        "angle": 0,
        "strokeColor": color,
        "backgroundColor": "transparent",
        "fillStyle": "solid",
        "strokeWidth": 2,
        "strokeStyle": dash,
        "roughness": 1,
        "opacity": 100,
        "groupIds": [],
        "frameId": None,
        "roundness": {"type": 2},
        "seed": _seed(),
        "version": 1, "versionNonce": _seed(),
        "isDeleted": False,
        "boundElements": [],
        "updated": int(time.time() * 1000),
        "link": None, "locked": False,
        "points": [[0, 0], [x2 - x1, y2 - y1]],
        "lastCommittedPoint": None,
        "startBinding": None, "endBinding": None,
        "startArrowhead": None, "endArrowhead": "arrow",
    }
    els.append(a)
    if label:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        els.append(text(mx - len(label) * 3, my - 18, label, size=11,
                        color=color, font=FONT_HAND))
    return els


def lane(x, y, w, h, title, color=C1):
    """A titled swim-lane container (faint border + header)."""
    els = []
    els.append(rect(x, y, w, h, stroke=color, bg="transparent", fill="hachure",
                    width=2, dash="dashed"))
    els.append(text(x + 14, y + 10, title, size=14, color=color, font=FONT_CODE))
    return els


def main():
    elements = []

    # Title
    elements.append(text(40, 24, "Boomatik Miniverse — Arquitectura", size=26,
                         color=C1, font=FONT_CODE))
    elements.append(text(40, 60,
                         "Visualizacion pixel-art del equipo de agentes BOO (Vite + TypeScript).",
                         size=13, color="#52525b", font=FONT_HAND))

    # --- Lane 1: Frontend (Vite) ---
    elements += lane(40, 100, 520, 360, "FRONTEND  ·  Vite + TypeScript", color=C1)

    n_index = node(70, 150, 200, 90, "index.html",
                   "HUD: cabecera, marcador,\nreloj, #app canvas mount", color=C1)
    n_main = node(70, 270, 200, 130, "src/main.ts",
                  "Entry. Genera tiles + sprites\nen canvas, monta Miniverse,\nfija polling /api/agents 3s", color=C1)
    n_core = node(330, 200, 200, 120, "@miniverse/core",
                  "Motor de render pixel.\nMiniverse(): escena, tiles,\nsprites, citizens, signal REST", color=C2)
    elements += n_index + n_main + n_core

    # --- Lane 2: Datos estaticos ---
    elements += lane(40, 480, 520, 150, "DATOS ESTATICOS  ·  en repo", color=C3)
    n_world = node(70, 520, 220, 90, "public/worlds/boomatik/\nworld.json",
                   "Grid 20x14, citizens,\nwanderPoints, props", color=C3)
    n_assets = node(320, 520, 210, 90, "tiles + sprites",
                    "Generados en runtime con\nCanvas API (sin imagenes)", color=C3)
    elements += n_world + n_assets

    # --- Lane 3: Backend (miniverse CLI) ---
    elements += lane(620, 100, 520, 530, "BACKEND  ·  @miniverse/server (CLI)", color=C2)

    n_server = node(650, 160, 230, 130, "miniverse (CLI)",
                    "Servidor REST de agentes\nlocalhost:4321\nscript npm: dev / server", color=C2)
    n_api = node(650, 320, 460, 170,
                 "API REST",
                 "POST /api/heartbeat  (registra/actualiza)\n"
                 "GET  /api/agents     (lista estado)\n"
                 "GET  /api/info\n"
                 "POST /api/act        (speak / mensaje)", color=C2)
    elements += n_server + n_api

    n_hooks = node(910, 160, 200, 130, "Claude Code hooks",
                   "settings.json:\nPreToolUse -> working\nPostToolUse -> thinking\nStop -> idle", color=C1)
    elements += n_hooks

    # --- Lane 4: Build / deploy ---
    elements += lane(620, 480, 520, 150, "BUILD / DEPLOY", color=C3)
    n_build = node(650, 520, 200, 90, "vite build -> dist/",
                   "bundle estatico", color=C3)
    n_deploy = node(890, 520, 220, 90, "team.boomatik.com",
                    "Railway / Vercel / VPS\n(coming soon)", color=C3)
    elements += n_build + n_deploy

    # --- Arrows ---
    elements += arrow(n_index[0], n_main[0], color=C1)
    elements += arrow(n_main[0], n_core[0], color=C1, label="monta")
    elements += arrow(n_world[0], n_main[0], color=C3, label="carga", dash="dotted")
    elements += arrow(n_assets[0], n_main[0], color=C3, dash="dotted")
    elements += arrow(n_core[0], n_api[0], color=C2, label="poll 3s /api/agents")
    elements += arrow(n_server[0], n_api[0], color=C2, label="sirve")
    elements += arrow(n_hooks[0], n_api[0], color=C1, label="heartbeat", dash="dashed")
    elements += arrow(n_main[0], n_build[0], color=C3, dash="dotted")
    elements += arrow(n_build[0], n_deploy[0], color=C3)

    # Honest note about scope
    elements.append(text(40, 660,
        "Nota de alcance honesta: proyecto pequeno. Sin DB, sin ORM, sin migraciones,\n"
        "sin llamadas a LLM dentro del repo. Frontend Vite consume una API REST local\n"
        "servida por la CLI de @miniverse/server. Los agentes BOO se muestran como\n"
        "jugadores (tema \"BOO FC stadium\"); su estado lo actualizan hooks de Claude Code.",
        size=12, color="#52525b", font=FONT_HAND))

    # Strip helper-only keys before serialising
    for el in elements:
        el.pop("_box", None)

    scene = {
        "type": "excalidraw",
        "version": 2,
        "source": "boomatik-miniverse/docs/gen_excalidraw.py",
        "elements": elements,
        "appState": {
            "gridSize": None,
            "viewBackgroundColor": "#ffffff",
        },
        "files": {},
    }

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "boomatik-miniverse-architecture.excalidraw")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(scene, f, ensure_ascii=False, indent=2)
    print(f"Wrote {out} with {len(elements)} elements")


if __name__ == "__main__":
    main()
