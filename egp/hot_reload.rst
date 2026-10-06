.. _doc_egp_hot_reload:

Runtime hot reload
==================

EGP supports opted-in C# and C++ reload in games launched by an editor build.
Set ``debug/hot_reload/enable_runtime=true`` before launching the game.
Export templates keep runtime reload disabled. C# uses collectible assemblies
when enabled; libraries that require non-collectible assemblies should retain
the default setting.

Building and reloading
----------------------

The C++ extension panel publishes successful Debug builds and notifies
attached games. C# Build sends the same debugger command. The game processes
native reload at an idle boundary before refreshing script bindings.
Failed compilation retains the previously published native descriptor/library.
Stop the game before Release extension builds.

Compatible changes can preserve native object identity, saved properties,
callables and subscriptions. Application threads must shut down through the
application's own lifecycle. Static state, arbitrary layouts and inheritance
changes require deliberate migration and validation.

Recovery and restart
--------------------

Missing or invalid libraries keep native parents and saved extension state
available for compatible repair. Changing a class's native base or removing
a live class requires repair or restart. Changing a method signature invalidates
cached native bindings; update callers. Dynamic lookup uses the repaired API,
while code holding raw cached bindings may need a restart.

Corrupted managed assemblies and blocked unloads have separate recovery paths.
Do not treat a successful single reload as long-session memory qualification.
See :doc:`cpp_extensions` and :doc:`api_contract` for the detailed contract and
the targeted ``validate_egp_hot_reload.py`` flags.

Native sessions after a clock fault
------------------------------------

The validator's opt-in ``--network-recovery`` case combines a native networking
clock fault with real C++/C# editor debugger reload. The qualified Windows Debug
run uses a separate editor and running-game process, with one authenticated
authority/client pair sharing the game process. Reload occurs after both native
sessions have stopped.

To reproduce the combined repair and networking gate with a new output prefix:

.. code-block:: powershell

   python misc/scripts/validate_egp_hot_reload.py `
       --engine bin/godot.windows.editor.dev.x86_64.mono.exe `
       --packages bin/GodotSharp/Tools/nupkgs `
       --assembly-recovery --unload-recovery `
       --native-recovery --native-abi-recovery --network-recovery `
       --output .build/network-reload-new

``--network-recovery`` requires runtime reload and cannot be combined with
``--disable-runtime``, ``--expect-disabled`` or ``--network-live-reload``. The validator creates a unique
child directory for commands, source/artifact hashes, editor/game identities,
samples and debugger diagnostics.

The authority misses 550 ms while the client continues native polling. The
authority returns ``FAILED`` and clears peers/entities; the client discovers
native disconnection, clears replicated state and is explicitly stopped. The
fixture then rebuilds C# and C++ and sends the real editor reload notification.
Both reloadable objects retain the same native session references and ObjectIDs
through serialized dictionaries. Native-session signals use method-name
Callables into the reconstructed objects. C++ uses generated session bindings;
C# uses the native ``GodotObject`` call API.

Poll calls work after reconstruction, stopped state remains empty and reload
does not implicitly restart authority. Explicit rebind and fresh-token admission
restart the same sessions on the original port. Retired peer sends and entity
updates fail; fresh ownership and opaque baselines match exactly. C++ and C#
application callbacks each occur once per admission, with authenticated sender
and byte payload checked. The resumed authority advances at least eight ticks.

The combined gate also passes assembly corruption/unload, missing/invalid DLL and
signature/base/ancestor/class repair checks. Stopped recovery and the
runtime-disabled baseline freshly pass with current fixture sources; the
disabled baseline retains its non-collectible assembly behavior.

This qualifies stopped native-session retention and explicit recovery.
Arbitrary managed facade or event
closure persistence, physics rollback during reload, independent-process
low-level fault/reload and exported-runtime reload remain unqualified. Raw
transport ownership does not authorize opaque gameplay messages. Exact receipts
and remaining scope are in the `pinned engine integration record
<https://github.com/ZSG-Studios/EGP/blob/4d43a101cf6a55e41c753720b089f348f72e58d2/doc/egp_integration_loop.md>`__.
See :doc:`language_testing` and :doc:`qualification` for the distinct networking
fixture evidence.

Live sessions during reload
----------------------------

``--network-live-reload`` keeps one authenticated authority/client pair connected
through failed builds and separate C#, C++ and combined reloads. The qualified
Windows Debug run uses a separate editor and running-game process; both native
sessions share that game process. Both outbound simulators are configured before
admission with 30 ms latency, 5 ms jitter and 5 percent loss.

.. code-block:: powershell

   python misc/scripts/validate_egp_hot_reload.py `
       --engine bin/godot.windows.editor.dev.x86_64.mono.exe `
       --packages bin/GodotSharp/Tools/nupkgs `
       --assembly-recovery --unload-recovery `
       --native-recovery --native-abi-recovery --network-live-reload `
       --network-latency-ms 30 --network-jitter-ms 5 --network-loss-percent 5 `
       --output .build/live-network-reload-new

Live mode requires runtime reload. Run it separately from ``--network-recovery``,
``--disable-runtime`` and ``--expect-disabled``. Set simulation options in live
mode: finite latency/jitter values are in 0–5000 ms and loss is a percentage in
0–100. Defaults are 30 ms, 5 ms and 5 percent respectively. Nondefault simulation
values outside live mode and invalid ranges are rejected before creating output.

.. list-table:: Live checkpoints
   :header-rows: 1
   :widths: 35 65

   * - Checkpoint
     - Required behavior
   * - Initial admission
     - Establish the owned baseline and native session references.
   * - Managed compiler failure
     - Retain the preceding live code and connection.
   * - Native compiler failure
     - Retain live code and the published descriptor.
   * - C# reload
     - Replace managed methods and advance managed deserialization.
   * - C++ reload
     - Replace native methods without managed deserialization.
   * - Combined reload
     - Replace both implementations and retain the connected pair.

Every checkpoint retains the same game process, native session ObjectIDs, port,
authenticated peer and replicated entity. Client history remains exactly
``Connecting -> Synchronizing -> Connected``: no stop, disconnect, new admission
or authority fault is permitted. Serialized native references and method-name
callbacks remain valid after reconstruction. Clocks, entity revisions and
language-driven polling advance at each stage.

Each checkpoint exchanges one application payload in each direction. Sender,
exact bytes, callback counts and the fresh owned baseline are checked. Both C++
and C# callbacks advance exactly from 1 through 6, without duplicates. These
checks cover transport and ownership metadata; gameplay authorization remains
the application's responsibility.

The full repair gate also passes. The current evidence suite passes 29 semantic
tests (14 stopped recovery and 15 live reload) and ten invalid CLI cases.
Configured loss does not measure actual dropped packets or real WAN behavior;
poll/tick counts establish fixture continuity, not performance.

Independent-process low-level fault/reload, deliberately in-flight callbacks or
concurrent reload, arbitrary managed facade/event closures or application/ABI
state, physics rollback during reload, exported-runtime reload, other platforms,
scale and soak remain unqualified. Consult the pinned integration record above
for exact source/artifact hashes, checkpoints and remaining acceptance items.
