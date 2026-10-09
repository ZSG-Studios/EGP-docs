# EGP documentation

EGP's manual and class reference, maintained by ZSG-Studios and forked from
[Godot's official documentation](https://github.com/godotengine/godot-docs).
The original Sphinx theme, code tabs, copy buttons, search and light/dark styles
are retained. `egp/` documents the fork-specific systems and migration paths.

## Build

```sh
python -m venv .venv
python -m pip install -r requirements.txt
python -m sphinx -b html -W --keep-going -j 4 . _build/html
python -m http.server 8070 --directory _build/html
```

Activate the virtual environment first (`.venv/Scripts/Activate.ps1` on Windows
or `source .venv/bin/activate` on Linux/macOS). The generated HTML is usable offline.
CI retains the complete HTML artifact. The manually triggered Pages workflow
publishes a separately checked build.

## Maintain the reference

Native class pages and canonical system guides are generated from the EGP engine.
Edit the engine XML/manual sources first. From this documentation checkout,
with a sibling engine checkout at the exact committed revision:

```sh
python tools/sync_egp_docs.py --engine ../EGP-Engine
python tools/sync_egp_docs.py --engine ../EGP-Engine --check
```

`egp/source_manifest.json` records the exact engine revision and normalized
source/output SHA256 hashes, including the documentation generator. The wrapper
uses the engine's native reference generator and adds complete public C#/C++
helper declarations, including multiline signatures and defaults. CI checks
these generated files against that pinned
engine checkout. Additional tutorials, navigation and presentation are edited
here. See `egp/reference_workflow.rst` for this fork's complete update workflow
and `egp/documentation.md` for the engine-source maintenance contract.

Keep an `upstream` remote for `https://github.com/godotengine/godot-docs.git`.
Review upstream merges for retired multiplayer/physics APIs before synchronizing
and building. The original upstream class-sync workflow is replaced with EGP's
manual sync, which exports a reviewable patch instead of overwriting the branch.

## License

The manual retains **CC BY 3.0** attribution to Juan Linietsky, Ariel Manzur and
the Godot community. Generated class reference files retain the engine's **MIT
license**. See [LICENSE.txt](LICENSE.txt). EGP additions are maintained by
ZSG-Studios; this is not the official Godot documentation service.
