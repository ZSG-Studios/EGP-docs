#!/usr/bin/env python3
"""Synchronize the EGP manual pages and class reference from an engine checkout."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

DOCS = Path(__file__).resolve().parents[1]


def consecutive_headings(text: str) -> str:
    """Retain Markdown heading hierarchy without skipping rendered levels."""
    result = []
    hierarchy: list[tuple[int, int]] = []
    fence = None
    for line in text.splitlines(keepends=True):
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)", line)
        if marker:
            token, suffix = marker.groups()
            if fence is None:
                fence = (token[0], len(token))
            elif token[0] == fence[0] and len(token) >= fence[1] and not suffix.strip():
                fence = None
            result.append(line)
            continue
        heading = re.match(r"^(#{1,6})[ \t]+", line) if fence is None else None
        if heading:
            source_level = len(heading[1])
            while hierarchy and hierarchy[-1][0] >= source_level:
                hierarchy.pop()
            rendered_level = hierarchy[-1][1] + 1 if hierarchy else source_level
            hierarchy.append((source_level, rendered_level))
            line = "#" * rendered_level + line[source_level:]
        result.append(line)
    return "".join(result)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--engine", type=Path, required=True)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    engine = args.engine.resolve()
    with tempfile.TemporaryDirectory(prefix="egp-reference-") as temporary:
        generated = Path(temporary)
        (generated / "egp").mkdir()
        (generated / "conf.py").touch()
        (generated / "egp/index.rst").touch()
        subprocess.run(
            [sys.executable, str(engine / "misc/scripts/sync_egp_docs.py"), "--docs", str(generated)], check=True
        )
        manifest = json.loads((generated / "egp/source_manifest.json").read_text(encoding="utf-8"))
        for name in manifest["generated_sha256"]:
            if name.endswith(".md"):
                guide = generated / name
                guide.write_text(consecutive_headings(guide.read_text(encoding="utf-8")), encoding="utf-8", newline="\n")
                manifest["generated_sha256"][name] = hashlib.sha256(guide.read_bytes()).hexdigest()
        manifest["documentation_generator_sha256"] = hashlib.sha256(
            Path(__file__).read_text(encoding="utf-8").encode("utf-8")
        ).hexdigest()
        (generated / "egp/source_manifest.json").write_text(
            json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n"
        )
        names = [*manifest["generated_sha256"], "egp/source_manifest.json"]
        changed = [
            name
            for name in names
            if not (DOCS / name).is_file() or (DOCS / name).read_bytes() != (generated / name).read_bytes()
        ]
        removed = [path for path in (DOCS / "classes").glob("class_*.rst") if "classes/" + path.name not in names]
        if args.check:
            if changed or removed:
                print("Documentation drift: " + ", ".join(changed + ["removed:" + path.name for path in removed]))
                return 1
        else:
            for name in changed:
                destination = DOCS / name
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes((generated / name).read_bytes())
            for path in removed:
                path.unlink()
        print(
            f"EGP documentation {'verified' if args.check else 'synchronized'} at {manifest['engine_revision']}."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
