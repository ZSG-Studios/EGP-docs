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

The published Windows runs pass all 27 validator steps and 197 interop assertions
each in the editor, relocated Debug and relocated Release. The fresh fixtures
supersede the preceding 60-, 93- and 133-assertion results. Native engine APIs, generated glue
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

Live clients and explicit rejoin
----------------------------------

High-level C# and C++ fault cycles retain authenticated UDP clients in the same
local process. During each authority polling gap, the client continues polling
and stays ``Connected``. The fixture then performs explicit recovery:

1. Observe the authority's native ``FAILED`` result and cleared state.
2. Stop the client, verify empty baselines and reject input while stopped with
   ``ERR_UNCONFIGURED``.
3. Restore the trusted Box3D checkpoint, rebind the authority's original port and
   attach its physics clock before starting admission.
4. Issue a fresh token and rejoin using the same retained client native session.

Attaching the physics clock before admission prevents the transport clock from
advancing while the restored world is detached. Each client records four exact
``Connecting -> Synchronizing -> Connected -> Stopped`` cycles: its initial
admission and three rejoins. Across editor/Debug/Release this qualifies 18
high-level live-client fault recoveries and 24 fresh admissions. Connected
low-level recovery is qualified separately below.

After rejoin, the client receives only a fresh owned entity mapped to the stable
physics body, with a tick after the restored checkpoint and continued falling
motion. Input for the retired handle is rejected; input for the fresh owned
handle is delivered exactly once. Hiding and showing the entity removes and
restores its client baseline, with zero invalid input callbacks.

Client outbound simulation uses 20 ms latency, 5 ms jitter and zero loss. This
bounded simulation does not establish bidirectional WAN behavior or soak.
Tokens and local snapshots stay outside the receipts.

Connected low-level sessions
----------------------------

Low-level C# and C++ fixtures now keep authenticated clients connected during
the three authority clock faults. This replaces the earlier no-peer low-level
cycles. Across editor/Debug/Release, they add 18 connected low-level recoveries
and 24 fresh admissions, including initial joins. The mixed high-/low-level
fixture therefore covers 36 connected recoveries and 48 admissions.

The client keeps polling through the authority's gap, detects native
``Disconnected``, verifies empty peers/entities and rejects application sends
with ``ERR_DOES_NOT_EXIST``. It explicitly stops and rejoins with a fresh token
on the same native session. The authority retains its native session and bound
port. Admission and disconnect histories require the same synchronization
stages: ``Connecting -> Synchronizing -> Connected`` for each admission, and
native ``Stopped -> Disconnected`` followed by explicit ``Stopped`` before rejoin.

Each rejoin advances the authenticated peer generation and creates a fresh owned
entity. Operations on retired handles must fail:

.. list-table:: Retired-handle checks
   :header-rows: 1
   :widths: 60 40

   * - Operation
     - Expected error
   * - Application send, disconnect or visibility using the retired peer
     - ``ERR_DOES_NOT_EXIST``
   * - Spawn with the retired peer as authority
     - ``ERR_INVALID_PARAMETER``
   * - Update the retired entity
     - ``ERR_DOES_NOT_EXIST``

Opaque baseline bytes are checked exactly, including zero and ``0xff``:
``0100ff2a``, ``0200ff2a`` and ``0300ff2a``. Each cycle exchanges one application
payload and one channel-3 ``ReliableOrdered`` packet in each direction. Callback
checks require the authenticated sender, channel/delivery and exact bytes, with
cumulative counts of 1/2/3 and no duplicates. Hide/show removes and restores the
identical baseline, and the resumed authority clock advances at least eight ticks.

These checks qualify raw transport and ownership metadata. Gameplay meaning and
authorization of opaque application messages remain the application's
responsibility. Each language uses one authority/client pair in one local
Windows process, with outbound client latency of 20 ms, jitter of 5 ms and zero
loss. Independent-process low-level faults require separate qualification.

Independent server stalls
-------------------------

The language validator also runs six independent authority/client process pairs:
C# and C++ clients in the editor, relocated Debug and relocated Release. Each
pair contains one GDScript authority and one authenticated client on local
Windows. This adds 18 server clock faults, 18 native client disconnects and
24 fresh admissions to the separate-process evidence.

The authority stops polling for at least 550 ms while the client continues
polling in its own process. After the native ``FAILED`` result, the authority
clears peers/entities, restores its trusted local Box3D checkpoint and rebinds
the same port/session with the physics clock attached. The client discovers
native ``Disconnected`` through polling, verifies an empty baseline and rejected
input, explicitly stops, then obtains a fresh fixture token and rejoins using
the same native session.

Each admission requires ``Connecting -> Synchronizing -> Connected``. The three
faults include native ``Stopped -> Disconnected``, followed by the fixture's
explicit ``Stopped`` before rejoin. Fresh owned entity handles and physics ticks
after the restored checkpoint are checked, together with exactly one owner input
per admission. Ownership uses the new authenticated peer handle. Stable physics
body 10000 persists through all three checkpoint restores.

To rerun one pair after building the isolated project with the language validator
above, choose a new, nonexistent output directory:

.. code-block:: powershell

   python misc/scripts/validate_egp_net_clock_process.py `
       --engine bin/godot.windows.editor.dev.x86_64.mono.exe `
       --project .build/language-qualification-new/project `
       --client-language cpp `
       --output .build/independent-clock-new

``--engine`` and ``--client-language`` are required; client choices are
``csharp`` and ``cpp``. For a packaged game, omit ``--project`` and point
``--engine`` to its matching relocated Mono executable. Omitting ``--output``
creates a unique run under ``.build/egp-net-clock-processes``. The runner captures
both child processes and terminates unfinished children when its watchdog expires.

The fixture refreshes tokens through a trusted temporary local handoff directory,
removed when the run ends. Receipts and logs contain no token bytes or physics
snapshots. This test policy demonstrates explicit recovery; production account
admission, token refresh and retry/backoff policy require their own implementation
and qualification.

Client outbound simulation remains 20 ms latency, 5 ms jitter and zero loss.
The evidence reader rejects shared PIDs, requires at least ten distinct client
observations during each stall and checks native disconnect/baseline histories.
The qualified runs recorded 33 or 34 distinct polls per gap. Poll observations
check fixture continuity and are not a networking performance benchmark.

Evidence and limits
-------------------

The validator records commands, source hashes, SDK archives, fixture assemblies
and extensions, exported runtime/PCK hashes and process identities. Its evidence
reader independently checks session retention, fresh handles, failure cycles,
physics clock offsets and exact diagnostics. Twenty-two language regression tests
passed, including rejection of paused clients, uncleared baselines, reused
admission, missing synchronization history, old client physics time, accepted
retired input and failed visibility restoration. Connected low-level negatives
also reject reused or accepted retired peer handles, corrupted opaque bytes,
duplicate application callbacks, missing channel delivery and absent native
disconnects.

Fourteen additional semantic tests check independent-process evidence, including
distinct PIDs, continuous client observations, timestamp consistency, native
disconnects, baseline clearance, fresh admission and owner input history.
This brings the language/process evidence tests to 36.

Explicit same-process high-/low-level reset/rejoin and independent-process
high-level disconnect discovery with fixture-controlled rejoin are qualified.
Production admission/backoff and recovery policy, independent-process low-level
faults, deliberately in-flight callback or concurrent reload,
process crashes and hard outages, larger authoritative worlds, arbitrary
application/ABI state recovery, other platforms, scale/soak and performance
require separate qualification. Existing encrypted separate-process networking
and reload results remain distinct checks.

The separate ``--network-recovery`` reload gate retains native sessions through
C++/C# reconstruction after both sessions stop following one local authority
fault. A separate ``--network-live-reload`` gate retains a connected pair across
failed builds and C#/C++ reload under configured latency/jitter/loss. See
:doc:`hot_reload`; these gates do not qualify deliberately in-flight callbacks,
concurrent reload or arbitrary managed facade/event closure persistence.

Adding ``--network-physics`` retains one explicit native Box3D world through
either reload mode. GDScript steps its stable body from the authority clock;
both reconstructed C++ and C# objects must match the same native body state,
tick and hash. Live reload keeps physics advancing without new admission.
Stopped recovery preserves the world, rejects a damaged local checkpoint without
changing state, explicitly restores trusted bytes and resumes with a clock offset
after fresh admission. The current gates cover one local Windows Debug pair and
one body; automatic client prediction/rollback remains separate work. See the
physics subsection of :doc:`hot_reload` for commands and precise scope.

The current 27-stage language run freshly builds the changed C# session helpers
and passes 197 assertions each in editor and relocated Debug/Release, including
the independent high-level process fault cycles. Separate editor-run reload
gates exercise low-level ``NetSession.DetachForReload()`` and
``NetSession.ResumeAfterReload(Dictionary)`` with explicit handler resubscription.
Both live and stopped gates perform 23 managed checks and keep all seven native
signal connection counts constant. High-level ownership and arbitrary captured
closures remain outside this contract; exported language compatibility does not
qualify exported-runtime reload. See :doc:`hot_reload` for the hook example.

Exact publication receipts and remaining acceptance items are listed in the
`pinned engine integration record
<https://github.com/ZSG-Studios/EGP/blob/bbc7d801f5f9f6aff7aa62f0e999db2c156a6698/doc/egp_integration_loop.md>`__.
See :doc:`qualification`, :doc:`explicit_world` and :doc:`admission_testing`.
