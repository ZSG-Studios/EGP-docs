#!/usr/bin/env python3
"""Synchronize EGP sources and render complete C#/C++ helper declarations."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import NamedTuple

DOCS = Path(__file__).resolve().parents[1]
LEXER = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[A-Za-z_]\w*|=>|::|[^\s]')


class Token(NamedTuple):
    value: str
    start: int
    end: int


def tokens(text: str) -> list[Token]:
    return [Token(m[0], m.start(), m.end()) for m in LEXER.finditer(text) if not m[0].startswith(("//", "/*"))]


def compact(text: str) -> str:
    # Keep string defaults intact while joining multiline declarations.
    return re.sub(
        r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|\s+', lambda m: " " if m[0].isspace() else m[0], text
    ).strip()


def matching(items: list[Token], start: int, opener: str = "{", closer: str = "}") -> int:
    depth = 0
    for index in range(start, len(items)):
        if items[index].value == opener:
            depth += 1
        elif items[index].value == closer:
            depth -= 1
            if depth == 0:
                return index
    raise ValueError(f"Unclosed {opener} at source offset {items[start].start}")


def boundary(items: list[Token], start: int, end: int) -> int:
    parens = brackets = braces = 0
    for index in range(start, end):
        value = items[index].value
        if parens == brackets == braces == 0 and value in (";", "{", "=>"):
            return index
        if value == "(":
            parens += 1
        elif value == ")":
            parens -= 1
        elif value == "[":
            brackets += 1
        elif value == "]":
            brackets -= 1
        elif value == "{":
            braces += 1
        elif value == "}":
            braces -= 1
    raise ValueError(f"Missing declaration boundary at source offset {items[start].start}")


def member_declarations(text: str, items: list[Token], start: int, end: int, cpp: bool, visible: bool) -> list[str]:
    result: list[str] = []
    cursor = start
    while cursor < end:
        if items[cursor].value == ";":
            cursor += 1
            continue
        if cpp and items[cursor].value in ("public", "protected", "private") and items[cursor + 1].value == ":":
            visible = items[cursor].value == "public"
            cursor += 2
            continue
        split = boundary(items, cursor, end)
        kind = items[split].value
        prefix = compact(text[items[cursor].start : items[split].start])
        public = visible if cpp else items[cursor].value == "public"
        has_parameters = any(t.value == "(" for t in items[cursor:split])
        if kind == ";":
            if public:
                result.append(prefix + ";")
            cursor = split + 1
        elif kind == "=>":
            # Expression bodies can contain nested calls/lambdas; skip as a unit.
            expression_end = boundary(items, split + 1, end)
            if items[expression_end].value != ";":
                raise ValueError("Unsupported expression-bodied declaration")
            if public:
                result.append(prefix + (";" if has_parameters else " { get; }"))
            cursor = expression_end + 1
        else:
            close = matching(items, split)
            cursor = close + 1
            if has_parameters:
                # Constructor initializer lists are implementation, not signatures.
                if public:
                    # A colon after the argument list introduces a base/member initializer.
                    prefix = re.sub(r"\)\s*:\s.*$", ")", prefix)
                    result.append(prefix + ";")
            elif not cpp and public:
                accessors = [
                    name for name in ("get", "set", "init") if any(t.value == name for t in items[split + 1 : close])
                ]
                if not accessors:
                    raise ValueError(f"Unsupported public property: {prefix}")
                declaration = prefix + " { " + " ".join(name + ";" for name in accessors) + " }"
                if cursor < end and items[cursor].value == "=":
                    finish = boundary(items, cursor, end)
                    initializer = compact(text[items[cursor].start : items[finish].end])
                    if "(" not in initializer:
                        declaration += " " + initializer
                    cursor = finish + 1
                result.append(declaration)
            else:
                # Braced field initializers, if present, terminate with a semicolon.
                if cursor < end and items[cursor].value == ";":
                    if public:
                        result.append(prefix + " " + compact(text[items[split].start : items[cursor].end]))
                    cursor += 1
    return result


def public_types(text: str, cpp: bool) -> list[tuple[str, str]]:
    items = tokens(text)
    cursor = 0
    limit = len(items)
    if cpp:
        cursor = next(i for i, t in enumerate(items) if t.value == "namespace")
        cursor = next(i for i in range(cursor, limit) if items[i].value == "{")
        limit = matching(items, cursor)
        cursor += 1
    result = []
    while cursor < limit:
        if items[cursor].value == "namespace" and cpp:
            opening = next(i for i in range(cursor, limit) if items[i].value == "{")
            cursor = matching(items, opening) + 1
            continue
        split = boundary(items, cursor, limit)
        header = items[cursor:split]
        type_index = next((i for i, t in enumerate(header) if t.value in ("class", "struct", "enum")), None)
        if type_index is None:
            cursor = matching(items, split) + 1 if items[split].value == "{" else split + 1
            continue
        public = cpp or header[0].value == "public"
        keyword = header[type_index].value
        name_index = type_index + 1
        if keyword == "enum" and header[name_index].value == "class":
            name_index += 1
        name = header[name_index].value
        prefix = compact(text[items[cursor].start : items[split].start])
        if items[split].value == ";":
            if public:
                result.append((name, prefix + ";"))
            cursor = split + 1
            continue
        close = matching(items, split)
        if public:
            if keyword == "enum":
                declaration = compact(text[items[cursor].start : items[close].end]) + (";" if cpp else "")
            else:
                members = member_declarations(text, items, split + 1, close, cpp, keyword == "struct")
                visibility = "public:\n" if cpp and keyword == "class" else ""
                declaration = (
                    prefix
                    + " {\n"
                    + visibility
                    + "\n".join("    " + member for member in members)
                    + "\n}"
                    + (";" if cpp else "")
                )
            result.append((name, declaration))
        cursor = close + 1
    return result


def helper_reference(engine: Path, base: str, revision: str) -> str:
    lines = [
        base.split("\nC#\n--\n", 1)[0].rstrip(),
        "",
        "C#",
        "--",
        "",
        "Use ``EGP.Networking``. Public declarations below retain overloads,",
        "default arguments, events and property accessors; method bodies are omitted.",
        "",
    ]
    for language, pattern, folder, cpp in (("csharp", "*.cs", "csharp", False), ("cpp", "*.hpp", "cpp", True)):
        if cpp:
            lines.extend(
                [
                    "C++",
                    "---",
                    "",
                    "Include ``addons/egp_net/cpp/egp_net.hpp`` and use ``egp::networking``.",
                    "Godot types are used throughout. Public declarations omit inline bodies and",
                    "private fields. Keep wrappers alive for callbacks, and construct, call and",
                    "destroy them on the same Godot thread.",
                    "",
                ]
            )
        for source in sorted((engine / "modules/egp_net" / folder).glob(pattern)):
            for name, declaration in public_types(source.read_text(encoding="utf-8"), cpp):
                path = source.relative_to(engine).as_posix()
                heading = ("egp::networking::" if cpp else "EGP.Networking.") + name
                lines.extend(
                    [
                        heading,
                        "~" * len(heading),
                        "",
                        f"`Source <https://github.com/ZSG-Studios/EGP/blob/{revision}/{path}>`__",
                        "",
                        f".. code-block:: {language}",
                        "",
                    ]
                )
                lines.extend("    " + line if line else "" for line in declaration.splitlines())
                lines.append("")
    lines.extend(
        [
            "Standalone native servers instead include ``modules/egp_net/net_core.h``",
            "and use ``egp::net::Session`` without the GDScript codec. See",
            ":doc:`networking_reference` for its distinct API contract.",
            "",
        ]
    )
    return "\n".join(lines)


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
        helper = generated / "egp/helper_reference.rst"
        helper.write_text(
            helper_reference(engine, helper.read_text(encoding="utf-8"), manifest["engine_revision"]),
            encoding="utf-8",
            newline="\n",
        )
        manifest["generated_sha256"]["egp/helper_reference.rst"] = hashlib.sha256(helper.read_bytes()).hexdigest()
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
            f"EGP documentation {'verified' if args.check else 'synchronized'} at {manifest['engine_revision']}, with complete typed helper declarations."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
