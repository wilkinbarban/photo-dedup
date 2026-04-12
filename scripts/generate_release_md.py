import argparse
import re
from pathlib import Path


CATEGORY_ORDER = ["Added", "Changed", "Fixed", "Documentation"]
CATEGORY_LABELS = {
    "en": {
        "Added": "Added",
        "Changed": "Changed",
        "Fixed": "Fixed",
        "Documentation": "Documentation",
    },
    "pt": {
        "Added": "Adicionado",
        "Changed": "Alterado",
        "Fixed": "Corrigido",
        "Documentation": "Documentacao",
    },
    "es": {
        "Added": "Anadido",
        "Changed": "Cambiado",
        "Fixed": "Corregido",
        "Documentation": "Documentacion",
    },
}


def extract_version_section(changelog_text: str, version: str):
    heading_re = re.compile(r"^## \[(?P<version>[^\]]+)\] - (?P<date>.+)$", re.MULTILINE)
    matches = list(heading_re.finditer(changelog_text))
    for idx, match in enumerate(matches):
        if match.group("version") != version:
            continue
        start = match.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(changelog_text)
        date = match.group("date").strip()
        return date, changelog_text[start:end]
    raise ValueError(f"Version {version} not found in CHANGELOG.md")


def parse_items(section_text: str):
    items = {k: [] for k in CATEGORY_ORDER}
    current = None
    for raw_line in section_text.splitlines():
        line = raw_line.strip()
        if line.startswith("### "):
            category = line[4:].strip()
            current = category if category in items else None
            continue
        if not current:
            continue
        if not line.startswith("- "):
            continue
        if line == "- _No changes yet._":
            continue
        items[current].append(line[2:].strip())
    return items


def render_highlights(items, lang: str) -> str:
    rendered = []
    for category in CATEGORY_ORDER:
        cat_items = items.get(category, [])
        if not cat_items:
            continue
        rendered.append(f"### {CATEGORY_LABELS[lang][category]}")
        for item in cat_items:
            rendered.append(f"- {item}")
        rendered.append("")

    if not rendered:
        if lang == "en":
            return "- No notable changes listed in CHANGELOG for this version."
        if lang == "pt":
            return "- Nenhuma mudanca relevante listada no CHANGELOG para esta versao."
        return "- No hay cambios destacados listados en CHANGELOG para esta version."

    while rendered and rendered[-1] == "":
        rendered.pop()
    return "\n".join(rendered)


def main():
    parser = argparse.ArgumentParser(description="Generate RELEASE.md from RELEASE.template.md and CHANGELOG.md")
    parser.add_argument("--version", required=True, help="Release version number (e.g., 1.0.5)")
    parser.add_argument("--changelog", default="CHANGELOG.md")
    parser.add_argument("--template", default="RELEASE.template.md")
    parser.add_argument("--output", default="RELEASE.md")
    args = parser.parse_args()

    changelog_path = Path(args.changelog)
    template_path = Path(args.template)
    output_path = Path(args.output)

    changelog_text = changelog_path.read_text(encoding="utf-8")
    template_text = template_path.read_text(encoding="utf-8")

    date, section = extract_version_section(changelog_text, args.version)
    items = parse_items(section)

    content = template_text
    content = content.replace("{{VERSION}}", args.version)
    content = content.replace("{{DATE}}", date)
    content = content.replace("{{HIGHLIGHTS_EN}}", render_highlights(items, "en"))
    content = content.replace("{{HIGHLIGHTS_PT}}", render_highlights(items, "pt"))
    content = content.replace("{{HIGHLIGHTS_ES}}", render_highlights(items, "es"))

    output_path.write_text(content.strip() + "\n", encoding="utf-8")
    print(f"Generated {output_path} for version {args.version}")


if __name__ == "__main__":
    main()
