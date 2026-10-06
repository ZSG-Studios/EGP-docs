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
``--disable-runtime`` or ``--expect-disabled``. The validator creates a unique
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
signature/base/ancestor/class repair checks. Fourteen semantic evidence tests
and two incompatible-option checks passed. The current runtime-disabled baseline
retains its non-collectible assembly behavior.

This qualifies stopped native-session retention and explicit recovery.
Active-connection reload under impairment, arbitrary managed facade or event
closure persistence, physics rollback during reload, independent-process
low-level fault/reload and exported-runtime reload remain unqualified. Raw
transport ownership does not authorize opaque gameplay messages. Exact receipts
and remaining scope are in the `pinned engine integration record
<https://github.com/ZSG-Studios/EGP/blob/ca35e9c266c1ffaa3163b80e7bc81199a65159e2/doc/egp_integration_loop.md>`__.
See :doc:`language_testing` and :doc:`qualification` for the distinct networking
fixture evidence.
