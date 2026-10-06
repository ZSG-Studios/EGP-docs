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

The optional public C# facade gate below transfers low-level ``NetSession``
ownership explicitly instead of retaining its managed wrapper.

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
closure persistence, automatic client physics rollback, independent-process
low-level fault/reload and exported-runtime reload remain unqualified. Raw
transport ownership does not authorize opaque gameplay messages. Exact receipts
and remaining scope are in the `pinned engine integration record
<https://github.com/ZSG-Studios/EGP/blob/bbc7d801f5f9f6aff7aa62f0e999db2c156a6698/doc/egp_integration_loop.md>`__.
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

The full repair gate also passes. The current evidence suite passes 64 semantic
tests and twelve invalid CLI cases, including physics and public C# handoff checks.
Configured loss does not measure actual dropped packets or real WAN behavior;
poll/tick counts establish fixture continuity, not performance.

Independent-process low-level fault/reload, deliberately in-flight callbacks or
concurrent reload, arbitrary managed facade/event closures or application/ABI
state, automatic client physics rollback, exported-runtime reload, other platforms,
scale and soak remain unqualified. Consult the pinned integration record above
for exact source/artifact hashes, checkpoints and remaining acceptance items.

Native physics state during reload
----------------------------------

Add ``--network-physics`` to either networking mode to include one explicit native
Box3D world. The option requires ``--network-live-reload`` or
``--network-recovery``; it is off by default. The fixture uses a dynamic box at
stable body ID 10000, 60 Hz, four substeps, one worker and gravity (0, -9.8, 0).
A GDScript authority-clock callback steps the world once per simulation tick.
The fixture's own bounded opaque baseline codec publishes body position,
velocity and physics tick. Peer payloads never become solver snapshots.

Run the two modes separately with fresh output prefixes:

.. code-block:: powershell

   python misc/scripts/validate_egp_hot_reload.py `
       --engine bin/godot.windows.editor.dev.x86_64.mono.exe `
       --packages bin/GodotSharp/Tools/nupkgs `
       --assembly-recovery --unload-recovery `
       --native-recovery --native-abi-recovery `
       --network-live-reload --network-physics `
       --network-latency-ms 30 --network-jitter-ms 5 --network-loss-percent 5 `
       --output .build/live-physics-reload-new

   python misc/scripts/validate_egp_hot_reload.py `
       --engine bin/godot.windows.editor.dev.x86_64.mono.exe `
       --packages bin/GodotSharp/Tools/nupkgs `
       --network-recovery --network-physics `
       --output .build/stopped-physics-reload-new

Both reloadable language objects retain the native world reference in serialized
dictionaries alongside their sessions. C++ generated ``EGPBox3DWorld`` bindings
and C# native ``GodotObject`` calls must agree exactly on position, rotation,
linear/angular velocity, tick and state hash after reconstruction. The native
world ObjectID, body ID and body count must remain unchanged.

In live mode, the same world and body advance through all six reload checkpoints
without a new admission. The qualified run records authority physics ticks
33, 133, 246, 452, 688 and 1000, with received client ticks 27, 126, 242, 448, 679
and 996. Authority physics time equals native network time; the received baseline
stays at or behind it. Both outbound simulators use the live configuration above.
These observations establish fixture continuity and state consistency.

In recovery mode, the fixture captures a trusted local checkpoint immediately
before the authority stall. Both sessions stop, the client clears obsolete
physics state and C#/C++ reload preserves the stopped world without advancing it.
The qualified checkpoint is tick 22, state hash ``21a31bd979e10a65`` and body
Y position 9999.333984375.

Before fresh admission, the fixture deliberately advances the world one step,
then attempts to restore damaged checkpoint bytes. ``ERR_FILE_CORRUPT`` (16)
must leave the changed world's tick and hash intact. Explicit restoration of the
original trusted bytes must recover the exact saved tick, hash and position.
Fresh admission maps a new network entity to the same body 10000 and rejects
retired peer/entity handles. The current facade-enabled run resumes at world tick
40 and the client receives tick 40, satisfying
``world_tick = checkpoint_tick + restarted_network_tick``.

Current physics-enabled live and stopped gates, physics-off live regression and
the runtime-disabled baseline pass. This qualifies one local Windows Debug
editor-run pair and one native body with a fixture stepper and codec. Trusted
authority restoration is explicit; automatic client prediction/rollback,
production checkpoint/admission policy, larger worlds, independent-process
low-level fault/reload, concurrent/in-flight reload and arbitrary facade,
closure or ABI state need separate qualification. Exported-runtime reload,
platform parity, scale/soak and performance remain open. Configured packet loss
does not quantify actual drops or WAN behavior. See :doc:`explicit_world` for
the public world API and :doc:`prediction` for game-provided replay callbacks.

C# session ownership and events
-------------------------------

``EGP.Networking.NetSession`` provides an explicit handoff for editor-run C#
reload. Call ``DetachForReload()`` in ``ISerializationListener.OnBeforeSerialize``
and save its dictionary capsule in an exported property. Call the static
``ResumeAfterReload(Dictionary)`` in ``OnAfterDeserialize``, then subscribe your
application event handlers again. Both operations belong on the original Godot
thread, as do polling and disposal.

.. code-block:: csharp

   using EGP.Networking;
   using Godot;

   public partial class GameSession : Node, ISerializationListener
   {
       [Export] public Godot.Collections.Dictionary SessionReload { get; set; } = new();
       private NetSession? session;

       public override void _Ready()
       {
           session = new();
           session.ApplicationReceived += Receive;
           // Configure and listen/connect here; check each returned Error.
       }

       private void Receive(long peer, byte[] payload) { /* Application message. */ }

       public void OnBeforeSerialize()
       {
           if (session == null) return;
           SessionReload = session.DetachForReload();
           session = null;
       }

       public void OnAfterDeserialize()
       {
           if (SessionReload.Count == 0) return;
           session = NetSession.ResumeAfterReload(SessionReload);
           session.ApplicationReceived += Receive;
       }

       public override void _ExitTree() => session?.Dispose();
   }

Detaching disconnects managed signal bridges and clears the old wrapper's event
subscriptions while keeping the native session alive. The old wrapper becomes
unusable; accessing it or detaching it again throws ``ObjectDisposedException``.
Disposing that wrapper later does not close the transferred session. Successful
restoration reconnects the typed bridges, takes ownership and clears the capsule.
Dispose the restored wrapper when its owner exits.

Missing, malformed, foreign or consumed capsules throw ``ArgumentException``;
``null`` throws ``ArgumentNullException``. Rejected capsules remain unchanged.
Copies cannot claim the same session twice. Capsules contain trusted local
native references and stay in memory: they are not disk checkpoints, network
payloads or admission tokens. Save application state separately in exported
properties. Application handlers are resubscribed explicitly; arbitrary captured
closures and high-level ``Net``, ``NetNode`` or ``NetBox3D`` ownership are not
automatically transferred.

Add ``--network-csharp-facade`` to either networking reload mode to exercise the
public API; the flag requires ``--network-live-reload`` or ``--network-recovery``
and is off by default. The current qualified runs also enable Box3D physics and
all repair checks:

.. code-block:: powershell

   python misc/scripts/validate_egp_hot_reload.py `
       --engine bin/godot.windows.editor.dev.x86_64.mono.exe `
       --packages bin/GodotSharp/Tools/nupkgs `
       --assembly-recovery --unload-recovery `
       --native-recovery --native-abi-recovery `
       --network-live-reload --network-physics --network-csharp-facade `
       --output .build/csharp-live-handoff-new

   python misc/scripts/validate_egp_hot_reload.py `
       --engine bin/godot.windows.editor.dev.x86_64.mono.exe `
       --packages bin/GodotSharp/Tools/nupkgs `
       --assembly-recovery --unload-recovery `
       --native-recovery --native-abi-recovery `
       --network-recovery --network-physics --network-csharp-facade `
       --output .build/csharp-stopped-handoff-new

Each facade fixture performs 23 managed checks, including invalid/copied claims,
detached-wrapper access, old-wrapper disposal, native identity, event disconnect
and fresh callbacks. All seven native signal connection counts remain constant
at each checkpoint, including quiet signals. Live application callback counts
advance exactly from 1 through 6 in each direction. Handoff/restore counts are
0, 0, 0, 1, 1, 2: failed compilation and C++-only reload do not transfer the
managed owner. Game logs check for stale delegate, capture and script errors.

Fresh 27-stage language validation also passes 197 interoperability assertions
each in the Windows Mono editor and relocated Debug/Release exports with the
changed helper sources. Exported language compatibility is distinct from runtime
reload, which remains editor-run only. High-level ownership, arbitrary closure
or ABI state, independent-process low-level fault/reload, concurrent/in-flight
reload and automatic client rollback remain outside this gate. See
:doc:`helper_reference`, :doc:`language_testing` and :doc:`qualification`.
