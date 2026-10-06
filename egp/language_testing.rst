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

The published Windows runs pass all 27 validator steps and 133 interop assertions
each in the editor, relocated Debug and relocated Release. The fresh fixtures
supersede the preceding 60- and 93-assertion results. Native engine APIs, generated glue
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
live-client fault recoveries and 24 fresh admissions. The low-level fault cycles
remain local with no peers.

After rejoin, the client receives only a fresh owned entity mapped to the stable
physics body, with a tick after the restored checkpoint and continued falling
motion. Input for the retired handle is rejected; input for the fresh owned
handle is delivered exactly once. Hiding and showing the entity removes and
restores its client baseline, with zero invalid input callbacks.

Client outbound simulation uses 20 ms latency, 5 ms jitter and zero loss. This
bounded simulation does not establish bidirectional WAN behavior or soak.
Tokens and local snapshots stay outside the receipts.

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
physics clock offsets and exact diagnostics. Sixteen semantic regression tests
passed, including rejection of paused clients, uncleared baselines, reused
admission, missing synchronization history, old client physics time, accepted
retired input and failed visibility restoration.

Fourteen additional semantic tests check independent-process evidence, including
distinct PIDs, continuous client observations, timestamp consistency, native
disconnects, baseline clearance, fresh admission and owner input history.
This brings the language/process evidence tests to 30.

Explicit same-process reset/rejoin and independent-process disconnect discovery
with fixture-controlled rejoin are qualified. Production admission/backoff and
recovery policy, connected low-level session faults, hot reload during faults,
process crashes and hard outages, larger authoritative worlds, arbitrary
application/ABI state recovery, other platforms, scale/soak and performance
require separate qualification. Existing encrypted separate-process networking
and reload results remain distinct checks.

Exact publication receipts and remaining acceptance items are listed in the
`pinned engine integration record
<https://github.com/ZSG-Studios/EGP/blob/3cbba2e8d28e4f9f7666d06064ab537abbd5c4f4/doc/egp_integration_loop.md>`__.
See :doc:`qualification`, :doc:`explicit_world` and :doc:`admission_testing`.
