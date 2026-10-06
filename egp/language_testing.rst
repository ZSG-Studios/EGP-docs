.. _doc_egp_language_testing:

Testing language interoperability and recovery
==============================================

``misc/scripts/validate_egp_net_languages.py`` builds the shipped C#/C++
fixtures, installs the language helpers and runs interoperability checks against
a matching Mono editor and optional Windows exports. It also exercises encrypted
separate-process C#, GDScript and C++ networking.

Run from the engine checkout. Use SDK libraries and Mono packages produced by
the same engine build. The following PowerShell command includes both packaged
configurations; replace the SDK and archive paths with your matching artifacts:

.. code-block:: powershell

   python misc/scripts/validate_egp_net_languages.py `
       --engine bin/godot.windows.editor.dev.x86_64.mono.exe `
       --sdk C:/path/to/matching/sdk `
       --sdk-library C:/path/to/Debug/egp_godot_cpp.lib `
       --release-sdk-library C:/path/to/Release/egp_godot_cpp.lib `
       --packages bin/GodotSharp/Tools/nupkgs `
       --template bin/godot.windows.template_debug.x86_64.mono.exe `
       --release-template bin/godot.windows.template_release.x86_64.mono.exe `
       --output .build/language-qualification-new

Keep a fresh output directory for each run. Do not substitute a Debug SDK archive
for the Release archive. See :doc:`cpp_extensions` for the SDK workflow.

Qualified scope
---------------

The published Windows runs pass all 21 validator steps and 93 interop assertions
each in the editor, relocated Debug and relocated Release. The fresh fixtures
supersede the preceding 60-assertion results. Native engine APIs, generated glue
and external helper declarations are unchanged in this source increment.

The C++ sample's ``poll()`` binding now returns the first high-/low-level native
error instead of discarding it. An isolated old/current DLL control confirms
that the preceding dynamic call returned NIL at a clock failure, while the
corrected call returns ``FAILED``. Both versions stop authority at the fault;
the change makes that error visible to sample callers. Check poll results at
application call sites.

Each C# and C++ high-level and low-level session experiences three successive
clock failures, with intentional polling gaps of at least 550 ms. This produces
12 faults per configuration and 36 across editor/Debug/Release. Every cycle checks:

* ``FAILED`` and the native catch-up diagnostic;
* cleared authority and rejected work while stopped;
* the same retained session and port after explicit recovery;
* a fresh entity handle, with the old handle absent and rejected.

High-level fixtures also detach the Box3D adapter, deliberately advance the
solver, restore a trusted local checkpoint with exact hash/tick equality, then
attach a fresh entity to the same stable body. Eight new authority ticks advance
the world from its checkpoint offset. Local snapshots are not sent over the
network or included in receipts.

Evidence and limits
-------------------

The validator records commands, source hashes, SDK archives, fixture assemblies
and extensions, exported runtime/PCK hashes and process identities. Its evidence
reader independently checks session retention, fresh handles, failure cycles,
physics clock offsets and exact diagnostics. Eight semantic regression tests
passed for these checks.

These repeated-fault cycles are local and have no connected remote peers.
Client reconnect and hot reload during the faults, larger authoritative worlds,
arbitrary application/ABI state recovery, other platforms, scale/soak and
performance require separate qualification. Existing encrypted separate-process
networking and reload results remain distinct checks.

Exact publication receipts and remaining acceptance items are listed in the
`pinned engine integration record
<https://github.com/ZSG-Studios/EGP/blob/943a033d076852d0d3c51961a43b360fdc0d31bc/doc/egp_integration_loop.md>`__.
See :doc:`qualification`, :doc:`explicit_world` and :doc:`admission_testing`.
