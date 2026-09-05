import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def check_internal_links():
    md_files = list(ROOT.glob("**/*.md"))
    broken_links = []
    total_links = 0
    link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')

    for md_file in md_files:
        if ".git" in md_file.parts:
            continue
        content = md_file.read_text(encoding="utf-8")
        for match in link_pattern.finditer(content):
            total_links += 1
            text, url = match.group(1), match.group(2)
            if url.startswith("http://") or url.startswith("https://") or url.startswith("#") or url.startswith("mailto:"):
                continue
            # Handle local file links (may have #anchor)
            target = url.split("#")[0]
            if not target:
                continue
            resolved = (md_file.parent / target).resolve()
            if not resolved.exists():
                broken_links.append((md_file.relative_to(ROOT), url, target))

    print(f"Total internal links checked: {total_links}")
    if broken_links:
        print(f"Found {len(broken_links)} broken internal link(s):")
        for f, u, t in broken_links:
            print(f"  In {f}: {u} -> cannot find {t}")
        return False
    else:
        print("All internal links resolved successfully!")
        return True

def check_places_structure():
    places_dir = ROOT / "places"
    place_files = [p for p in places_dir.rglob("*.md") if p.name != "README.md"]
    print(f"Found {len(place_files)} destination place files in places/")
    missing_sections = []

    required_keywords = [
        "Circuit role",
        "Logistics",
        "Crowd",
    ]

    for p in place_files:
        content = p.read_text(encoding="utf-8")
        for kw in required_keywords:
            if kw.lower() not in content.lower():
                missing_sections.append((p.relative_to(ROOT), kw))

    if missing_sections:
        print(f"Found {len(missing_sections)} missing structural element(s):")
        for f, kw in missing_sections:
            print(f"  In {f}: missing section matching '{kw}'")
        return False
    else:
        print("All destination place files satisfy structural and logistics requirements!")
        return True

if __name__ == "__main__":
    links_ok = check_internal_links()
    places_ok = check_places_structure()
    if links_ok and places_ok:
        print("SUCCESS: Itinerary validation passed 100%!")
        sys.exit(0)
    else:
        print("FAILURE: Validation checks failed.")
        sys.exit(1)
