.. _doc_egp_admission_testing:

Testing admission across listener restarts
==========================================

``misc/scripts/validate_egp_net_admission.py`` tests the native session and
GDScript facade against controlled listener restart boundaries. It distinguishes
token timestamp rejection from secure-key rotation. Use matching binaries
from the qualified source and run from the engine repository:

.. code-block:: powershell

   python misc/scripts/validate_egp_net_admission.py --engine bin/godot.windows.editor.dev.x86_64.mono.exe --api both --key all --boundary both --fault both

This selects 24 cases: two APIs, three key modes, two timestamp boundaries and
two restart paths. The default fault selection is ``clock``; select ``both``
to also test graceful stop/rebind.

.. list-table:: Case selection
   :header-rows: 1
   :widths: 30 30 40

   * - Option
     - Values / default
     - Purpose
   * - ``--api``
     - ``native``, ``gdscript``, ``both`` / ``both``
     - Select native ClassDB calls or the installed GDScript facade.
   * - ``--key``
     - ``zero``, ``nonzero``, ``generated``, ``all`` / ``all``
     - Compare retained test patterns with a newly generated listener key.
   * - ``--boundary``
     - ``same``, ``cross``, ``both`` / ``both``
     - Compare token creation in the listener's restart second or before it.
   * - ``--fault``
     - ``clock``, ``graceful``, ``both`` / ``clock``
     - Exceed the fixed-clock budget or stop/rebind normally.
   * - ``--engine``
     - Required executable path
     - Run an editor or a matching Windows export template.
   * - ``--editor``
     - Optional matching source editor
     - Export a fresh isolated project when testing a template.
   * - ``--output``
     - ``.build/egp-admission-lifecycle``
     - Retain each run in a unique evidence directory.

For a packaged Debug game:

.. code-block:: powershell

   python misc/scripts/validate_egp_net_admission.py --engine bin/godot.windows.template_debug.x86_64.mono.exe --editor bin/godot.windows.editor.dev.x86_64.mono.exe --fault both

Use the matching ``template_release`` executable for Release qualification.
The recorded Windows qualification passed 24 cases each in the editor, Debug
and Release exports. This matrix exercises native and GDScript admission;
C#/C++ helper interoperability has its own fixtures and receipts.

Expected behavior
-----------------

With a retained zero/nonzero test key, an unused token created in the restart
second must connect. A token created before that second must fail the listener's
timestamp gate. Generated keys must reject both timings; the same-second case
isolates key rotation from timestamp protection.

The validator records public token creation/expiry timestamps and the listener's
restart boundary, checks unused account admission with free slots, and rejects
cases that miss the requested boundary. Token lifetime must match the listener's
configured maximum. Token and key bytes stay in memory.

Receipts include exact commands, process identities, logs and engine hashes.
Packaged tests also retain the exported runtime and PCK hashes. A clock failure
must produce the catch-up diagnostic; graceful restart must not. Rejected
admission must not reach synchronization or entity state.

These are bounded local lifecycle tests. A listener restart with a retained
key is not a general revocation mechanism; production identity, token delivery
and backend revocation require their own design and evidence. Historical
controls without timestamps cannot establish which rejection path occurred.
See :doc:`networking`, :doc:`network_lab` and :doc:`qualification`.
