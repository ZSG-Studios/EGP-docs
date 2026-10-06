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
<https://github.com/ZSG-Studios/EGP/blob/153dd599e9127d8c86f81fcafa1bdd4ab8168bb6/doc/egp_integration_loop.md>`__.
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
mode: finite latency/jitter values range from 0 to 5000 ms and loss ranges from
0 to 100 percent. Defaults are 30 ms, 5 ms and 5 percent respectively. Nondefault simulation
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

The full repair gate also passes. The current evidence suite passes 662 semantic
tests and eighteen invalid CLI cases, including low-level ownership, physics and
high-level C# node checks.
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
without a new admission. The preceding full physics/facade run records authority physics ticks
33, 133, 246, 452, 688 and 1000, with received client ticks 27, 126, 242, 448, 679
and 996. Authority physics time equals native network time; the received baseline
stays at or behind it. Both outbound simulators use the live configuration above.
These observations establish fixture continuity and state consistency.

In recovery mode, the fixture captures a trusted local checkpoint immediately
before the authority stall. Both sessions stop, the client clears obsolete
physics state and C#/C++ reload preserves the stopped world without advancing it.
The preceding full physics/facade gate's checkpoint is tick 22, state hash ``21a31bd979e10a65`` and body
Y position 9999.333984375.

Before fresh admission, the fixture deliberately advances the world one step,
then attempts to restore damaged checkpoint bytes. ``ERR_FILE_CORRUPT`` (16)
must leave the changed world's tick and hash intact. Explicit restoration of the
original trusted bytes must recover the exact saved tick, hash and position.
Fresh admission maps a new network entity to the same body 10000 and rejects
retired peer/entity handles. That facade-enabled run resumes at world tick
40 and the client receives tick 40, satisfying
``world_tick = checkpoint_tick + restarted_network_tick``.

The preceding full physics-enabled live/stopped gates pass, with fresh low-level
facade/physics live and runtime-disabled regressions at the current source.
This qualifies one local Windows Debug
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
automatically transferred by the low-level capsule. High-level C# ``NetNode``
has the separate serialization contract below.

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

High-level C# node reload
-------------------------

Keep ``EGP.Networking.NetNode`` in the scene tree and preserve its reference in
the owner's exported ``NetNode`` property. Its serialization hooks disconnect
forwarding without closing the GDScript codec child or native session, then
reconnect that same child. All eleven forwarding signals use named Godot methods.
The owner's ordinary C# application events must resubscribe after reload;
registered message handlers should retain a named Godot object/method target.

.. code-block:: csharp

   using EGP.Networking;
   using Godot;

   public partial class NetworkOwner : Node, ISerializationListener
   {
       [Export] public NetNode? Network { get; set; }

       public override void _Ready()
       {
           Network ??= new NetNode();
           if (Network.GetParent() == null) AddChild(Network);
           SubscribeEvents();
           Error error = Network.RegisterMessage("notice",
               new Callable(this, nameof(ReceiveNotice)), Sender.Server);
           if (error != Error.Ok) GD.PushError(error.ToString());
           // Configure and host/join explicitly; check each returned Error.
       }

       private void SubscribeEvents()
       {
           if (Network == null) return;
           Network.StateChanged -= OnState;
           Network.StateChanged += OnState;
       }

       private void OnState(string state) { /* Update application state. */ }
       private void ReceiveNotice(long peer, Godot.Collections.Array arguments)
       { /* Validate and handle the application message. */ }
       public void OnBeforeSerialize() { /* Save other exported state. */ }
       public void OnAfterDeserialize() => SubscribeEvents();
   }

Derived ``NetNode`` serialization overrides must call ``base`` so the helper can
detach and restore its own forwarding. Store application state separately:

.. code-block:: csharp

   using EGP.Networking;

   public partial class GameNetNode : NetNode
   {
       public override void OnBeforeSerialize()
       {
           // Save application-owned exported state here.
           base.OnBeforeSerialize();
       }

       public override void OnAfterDeserialize()
       {
           base.OnAfterDeserialize();
           // Restore application state and subscribe application handlers here.
       }
   }

Leaving the tree closes the session and disconnects all forwarding callbacks.
Reentry reconnects the existing codec child exactly once; host or join explicitly
to start a new session. Reconfigure custom options before that host/join operation.
Replacing a freed codec child restores forwarding and
the ``AutoPoll`` policy. The qualified lifecycle checks require eleven connection
counts of 1 before exit, 0 after exit and 1 after reentry, the same node/codec
identities, one child, closed sessions and empty peer/entity caches. Six additional
managed runtime checks cover codec replacement, event counts, raw packet bytes,
channel/delivery and retained manual polling. The current gate also qualifies
three explicit fresh-session traffic cycles after reentry, as described below.

Use ``--network-csharp-node`` with either networking reload mode. It is off by
default and requires ``--network-live-reload`` or ``--network-recovery``. Run it
separately from ``--network-csharp-facade`` and ``--network-physics``; those
combinations are rejected before output creation.

.. code-block:: powershell

   python misc/scripts/validate_egp_hot_reload.py `
       --engine bin/godot.windows.editor.dev.x86_64.mono.exe `
       --packages bin/GodotSharp/Tools/nupkgs `
       --assembly-recovery --unload-recovery `
       --native-recovery --native-abi-recovery `
       --network-live-reload --network-csharp-node `
       --output .build/csharp-node-live-new

   python misc/scripts/validate_egp_hot_reload.py `
       --engine bin/godot.windows.editor.dev.x86_64.mono.exe `
       --packages bin/GodotSharp/Tools/nupkgs `
       --assembly-recovery --unload-recovery `
       --native-recovery --native-abi-recovery `
       --network-recovery --network-csharp-node `
       --output .build/csharp-node-stopped-new

The live gate retains node, codec and native session identities and admission
across failed managed/native compilation and C#-only, C++-only and combined
reload. Six exchanges in each direction verify messages, named handlers,
owned input and raw packet contents; unowned input is rejected. Restores are
0, 0, 0, 1, 1, 2. The stopped gate keeps clients polling during the 550 ms
authority gap, reloads before explicit fresh admission and rejects retired
peer/entity handles. Both are one local Windows Debug pair sharing a game process.

Generic corrupted-assembly, blocked-unload and incompatible/missing native-class
repair checks run before network nodes are created. Those injected failures
during authenticated ``NetNode`` traffic remain unqualified. High-level C++
adapter ownership, arbitrary captured closures or game/ABI state,
independent-process low-level reload, concurrent/in-flight or exported-runtime
reload, automatic client physics rollback, platform/scale/soak and performance
remain open. Configured loss does not measure actual drops or WAN behavior.

Native session lifetime and reentry
-----------------------------------

The shared GDScript codec disconnects all seven callbacks when ``close()``
releases its native session. ``stop()`` retains the configured session and
callbacks for explicit restart. GDScript ``EGPNet``, C# ``NetNode`` and C++ ``Net``
share this codec; see :doc:`networking` for the corresponding language APIs.
Registered message handlers and scene factories remain on the codec.

Each current high-level live/stopped fixture runs three fresh-session cycles
after tree reentry. They retain the node/codec identities and one codec child,
reapply options, host on the released port, issue fresh tokens and join. All seven
callbacks on each retired native session must be zero; each fresh native signal
has one callback and all eleven typed forwarding connections remain exactly one.
Every new native session must differ from all retired sessions.

Exact typed messages, named handlers, owned inputs and raw packets must work
after each admission, with unowned input rejected and native ticks advancing.
Local stale packet/state injection on a retained retired native reference must
leave new typed packet counts and the current codec entity cache unchanged.
This is a local lifetime test, not a remote-attack or WAN security qualification.

Numeric peer/entity IDs can repeat in distinct native sessions. Save their
issuing session identity and discard ownership commands from retired sessions.
This differs from restarting a retained native session after a fixed-clock fault,
which preserves that session's handle generations. Application C# events still
resubscribe explicitly; named message handlers keep their target on the codec.

Eighteen managed runtime checks per fixture cover replacement from close/stop
state callbacks: a fresh listening session and its spawned entity must survive
the outer operation. The six freed-codec replacement checks also pass. This
qualifies those specific state-callback paths; arbitrary in-flight lifecycle
mutation remains open.

The commands above exercise the new cycles with current fixture sources. Fresh
27-stage language validation passes 197 assertions each in Windows editor and
relocated Debug/Release exports. Fresh evidence also covers 72 admission cases,
seven physics/network lab cases, visible three-client listen-host/dedicated runs,
the updated default GDScript sample, low-level facade/Box3D and runtime-default
regressions. Native engine, SDK/ClassDB/glue and installed binary identities are
unchanged.

Authenticated-node assembly/unload/ABI failures, high-level C++ adapter
ownership, independent-process low-level reload, concurrent/exported-runtime
reload, automatic client physics rollback, arbitrary closure/game state,
production admission/checkpoint policy and platform/scale/soak/performance
remain separate qualification work. Configured impairment does not measure
actual packet drops or WAN performance. The pinned integration record lists
exact commands, source/artifact hashes and remaining acceptance items.

C# Box3D adapter ownership
------------------------------

``NetBox3D.DetachForReload()`` transfers the existing GDScript adapter, attached
world and stable entity-to-body mapping into a trusted local capsule. The adapter
keeps its connection to the network clock. The old managed wrapper disconnects
its three named signal bridges, clears application events and becomes disposed.
Accessing it again throws ``ObjectDisposedException``; disposing it again cannot
detach the transferred adapter.

Consume the capsule with ``NetBox3D.ResumeAfterReload(Dictionary)`` on the
original Godot thread, then resubscribe application handlers. Successful resume
clears the capsule. Null throws ``ArgumentNullException``; malformed, future,
foreign or consumed claims throw ``ArgumentException`` without changing them.
Copies cannot reclaim consumed ownership. Ordinary disposal detaches the adapter;
the caller retains ownership of the world and network node. Capsules contain
local object references and are not disk/network checkpoints or client rollback.

.. code-block:: csharp

   using EGP.Networking;
   using Godot;

   public partial class PhysicsOwner : Node, ISerializationListener
   {
       [Export] public Godot.Collections.Dictionary AdapterReload { get; set; } = new();
       private NetBox3D? adapter;

       // Call once after the application creates its network node and world.
       public Error AttachWorld(NetNode network, GodotObject world)
       {
           adapter?.Dispose();
           adapter = new NetBox3D();
           adapter.AfterStep += AfterStep;
           return adapter.Attach(network, world);
       }

       private void AfterStep(long tick) { /* Observe the completed world step. */ }

       public void OnBeforeSerialize()
       {
           if (adapter == null) return;
           AdapterReload = adapter.DetachForReload();
           adapter = null;
       }

       public void OnAfterDeserialize()
       {
           if (AdapterReload.Count == 0) return;
           adapter = NetBox3D.ResumeAfterReload(AdapterReload);
           adapter.AfterStep += AfterStep;
       }

       public override void _ExitTree() => adapter?.Dispose();
   }

Add ``--network-csharp-box3d`` to either networking reload mode alongside
``--network-csharp-node``. It is off by default and cannot be combined with
``--network-physics`` or ``--network-csharp-facade``:

.. code-block:: powershell

   python misc/scripts/validate_egp_hot_reload.py `
       --engine bin/godot.windows.editor.dev.x86_64.mono.exe `
       --packages bin/GodotSharp/Tools/nupkgs `
       --network-live-reload --network-csharp-node --network-csharp-box3d `
       --assembly-recovery --unload-recovery --native-recovery --native-abi-recovery `
       --output .build/box3d-live-handoff-new

   python misc/scripts/validate_egp_hot_reload.py `
       --engine bin/godot.windows.editor.dev.x86_64.mono.exe `
       --packages bin/GodotSharp/Tools/nupkgs `
       --network-recovery --network-csharp-node --network-csharp-box3d `
       --assembly-recovery --unload-recovery --native-recovery --native-abi-recovery `
       --output .build/box3d-stopped-handoff-new

Fresh live/stopped fixtures retain the same adapter, world and stable body 10000.
Each completed world tick has one before/after event; all three managed signals
have one connection, the adapter has one clock connection and no adapter failures
occur. C++ and C# reads agree on the world state. The live gate covers six reload
phases; the stopped gate retains unchanged physics through reload, then advances
after explicit fresh admission. Both cover tree exit/reentry and three new-session
cycles, remapping the new entity to the retained body. Twenty-two managed capsule
checks per fixture cover ownership and rejection behavior.

Debugger fixture commands and native reload requests defer until the active
poll/tick call returns. Preserved failing controls demonstrate that synchronous
test mutations inside an unfinished tick could overwrite entity state or
interrupt stepping. These gates qualify operations at that boundary. Arbitrary
application mutation inside callbacks and general in-flight reload remain open.

Fresh 27-stage trilingual validation passes 197 assertions in each editor,
Debug and Release configuration. The low-level facade/world and default runtime
regressions also pass. The native engine, SDK, ClassDB and managed glue retain
their unchanged identities. Seven GDS-only physics/lab cases and 72 admission
cases reuse byte-identical executed inputs; fresh C# builds supersede their unused
historical C# helper manifest entry. Reload remains one local Windows Debug pair
sharing a game process. High-level C++ adapter ownership, authenticated-node
assembly/unload/ABI failures, concurrent/exported-runtime reload, automatic client
rollback, production checkpoint policy and broader platform/scale/performance
still require qualification.
