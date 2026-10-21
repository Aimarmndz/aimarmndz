"""Genera los badges estáticos del perfil en assets/badges/.

Se versionan como SVG para no depender de shields.io: GitHub pasa las imágenes
externas por su proxy (camo) y a veces las corta, dejando badges rotos.

Uso: python3 scripts/build_badges.py
"""

from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets" / "badges"

# Fuente monoespaciada para poder calcular el ancho sin métricas de fuente.
# textLength fuerza ese ancho aunque el sistema del visitante use otra fuente.
FONT = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"
CHAR_ADVANCE = 0.6  # ancho de un carácter monoespaciado en em
TRACKING = 0.6  # px extra por carácter, el letter-spacing de la maqueta

THEMES = {
    "dark": {
        "chip": "#21262d",
        "border": "#30363d",
        "text": "#e6edf3",
        "label": "#9198a1",
        "pill": "#e6edf3",
        "pill_text": "#0d1117",
    },
    "light": {
        "chip": "#f6f8fa",
        "border": "#d1d9e0",
        "text": "#1f2328",
        "label": "#59636e",
        "pill": "#1f2328",
        "pill_text": "#ffffff",
    },
}

# Iconos de trazo en una rejilla de 24x24, los mismos que la maqueta
ICONS = {
    "globe": '<circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15 15 0 0 1 0 20M12 2a15 15 0 0 0 0 20"/>',
    "linkedin": '<rect x="2" y="2" width="20" height="20" rx="3"/><path d="M7 10v7M7 7v.01M11 17v-7M11 13a3 3 0 0 1 6 0v4"/>',
    "mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 6-10 7L2 6"/>',
    "chat": '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>',
    "cup": '<path d="M17 8h1a4 4 0 1 1 0 8h-1M3 8h14v9a4 4 0 0 1-4 4H7a4 4 0 0 1-4-4zM6 2v2M10 2v2M14 2v2"/>',
}

CONTACT = [
    ("portfolio", "globe", "aimar.dev"),
    ("linkedin", "linkedin", "LinkedIn"),
    ("email", "mail", "contact@aimar.dev"),
    ("discord", "chat", "Discord"),
]

STACK = [
    ("infra", "infra & cloud", ["Docker", "Kubernetes", "Google Cloud", "Linux", "macOS"]),
    ("databases", "databases", ["MySQL", "PostgreSQL"]),
    ("languages", "languages", ["Bash", "Python", "TypeScript", "JavaScript", "C++", "Lua"]),
    ("tools", "frameworks & tools", ["Node.js", "Next.js", "React", "FastAPI", "Tailwind", "shadcn/ui", "Git", "VS Code"]),
]

STACK_LABEL_WIDTH = 168


def text_width(text: str, size: float) -> float:
    return len(text) * (size * CHAR_ADVANCE + TRACKING)


def text(x: float, y: float, value: str, size: float, fill: str, weight: int = 400, anchor: str = "start") -> str:
    width = text_width(value, size)
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FONT}" font-size="{size}" font-weight="{weight}" '
        f'fill="{fill}" text-anchor="{anchor}" textLength="{width:.1f}" lengthAdjust="spacingAndGlyphs">'
        f"{escape(value)}</text>"
    )


def icon(name: str, x: float, y: float, size: float, color: str) -> str:
    scale = size / 24
    return (
        f'<g transform="translate({x:.1f} {y:.1f}) scale({scale:.4f})" fill="none" stroke="{color}" '
        f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</g>'
    )


def svg(width: float, height: float, title: str, body: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}" height="{height:.0f}" '
        f'viewBox="0 0 {width:.0f} {height:.0f}" role="img" aria-label="{escape(title)}">'
        f"<title>{escape(title)}</title>{body}</svg>\n"
    )


def contact_badge(icon_name: str, label: str, theme: dict) -> str:
    value = label.upper()
    pad, icon_size, gap, height = 12, 14, 8, 32
    width = pad + icon_size + gap + text_width(value, 12) + pad
    body = (
        f'<rect x="0.5" y="0.5" width="{width - 1:.1f}" height="{height - 1}" rx="6" '
        f'fill="{theme["chip"]}" stroke="{theme["border"]}"/>'
        + icon(icon_name, pad, (height - icon_size) / 2, icon_size, theme["text"])
        + text(pad + icon_size + gap, 20.2, value, 12, theme["text"], 600)
    )
    return svg(width, height, label, body)


def stack_row(label: str, items: list[str], theme: dict) -> str:
    # Margen vertical dentro del SVG: en el README las filas van seguidas con <br />
    pad, gap, height, top = 8, 6, 24, 5
    parts = [text(0, top + 16.5, label, 13, theme["label"])]
    x = STACK_LABEL_WIDTH
    for item in items:
        value = item.upper()
        chip = pad + text_width(value, 11) + pad
        parts.append(
            f'<rect x="{x + 0.5:.1f}" y="{top + 0.5}" width="{chip - 1:.1f}" height="{height - 1}" rx="4" '
            f'fill="{theme["chip"]}" stroke="{theme["border"]}"/>'
        )
        parts.append(text(x + pad, top + 16, value, 11, theme["text"], 600))
        x += chip + gap
    return svg(x - gap, height + 2 * top, f"{label}: {', '.join(items)}", "".join(parts))


def kofi_badge(theme: dict) -> str:
    label = "Support me on Ko-fi"
    pad, icon_size, gap, height = 16, 16, 8, 36
    width = pad + icon_size + gap + text_width(label, 14) + pad
    body = (
        f'<rect width="{width:.1f}" height="{height}" rx="18" fill="{theme["pill"]}"/>'
        + icon("cup", pad, (height - icon_size) / 2, icon_size, theme["pill_text"])
        + text(pad + icon_size + gap, 22.8, label, 14, theme["pill_text"], 600)
    )
    return svg(width, height, label, body)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    files = {}
    for mode, theme in THEMES.items():
        for slug, icon_name, label in CONTACT:
            files[f"{slug}-{mode}.svg"] = contact_badge(icon_name, label, theme)
        for slug, label, items in STACK:
            files[f"stack-{slug}-{mode}.svg"] = stack_row(label, items, theme)
        files[f"kofi-{mode}.svg"] = kofi_badge(theme)
    for name, content in files.items():
        (OUT / name).write_text(content, encoding="utf-8")
    print(f"{len(files)} badges en {OUT}")


if __name__ == "__main__":
    main()
