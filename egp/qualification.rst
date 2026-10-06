.. _doc_egp_qualification:

Support and qualification
=========================

EGP is a development fork based on Godot 4.8-dev. The source implements the
systems below; qualification applies to the binaries, platforms and fixtures
identified in the engine's receipts. Build success and API exposure alone do
not establish runtime behavior or production readiness.

.. list-table:: Current scope
   :header-rows: 1
   :widths: 25 45 30

   * - System
     - Documented integration
     - Further qualification
   * - Box2D/Box3D
     - Sole native scene backends; fixed-profile physics; explicit Box3D worlds
     - Broad shape, character, joint and scene parity; platform and performance matrix
   * - Networking
     - Yojimbo encrypted admission; authoritative bounded state; ownership and interest
     - Production authentication, large worlds, bandwidth scaling and soak
   * - Prediction
     - Bounded game-provided capture/restore/replay
     - Complete game input acknowledgments, collision corrections and lag compensation
   * - C++ tooling
     - Embedded SDK, editor scaffold/build, diagnostics and Debug/Release publication
     - Arbitrary ABI changes, additional platforms and long-session reload
   * - Runtime reload
     - Opted-in editor-run C#/C++ reload and targeted failure recovery
     - Broader script types, static state, thread lifetime and memory behavior
   * - Builds/exports
     - Windows x64 native/Mono editors and matching template workflows
     - Other-platform, release and rendering features require their own receipts

The networking lab covers bounded local dedicated/listen-host processes,
outgoing impairment, fresh admission after reconnect/stalls, same-process
listener recovery and explicit checkpoint-based server replacement. Server-gap
receipts check fresh keys/tokens, retired admission and input rejection, new
ownership and restoration of the fixture's counter. The opt-in ``--physics``
fixture adds trusted local Box3D checkpoint restoration, transactional rejection
of damaged snapshots, six-tick replay and stable entity-to-body mapping.
Arbitrary game-state restoration, larger authoritative worlds and automatic
client physics rollback require separate qualification.
It is an application fixture, not a
production identity service or automatic server persistence.

Fresh C#/C++ fixtures pass 197 interoperability assertions each in the Windows
Mono editor and relocated Debug/Release exports. They include three successive
clock failures per language on both high-level and low-level sessions: 36 local
faults across those configurations. Each cycle checks the native failure,
retained session/port, retired handles and explicit recovery. High-level fixtures
also restore trusted local Box3D checkpoints and map fresh entities to stable
bodies. These results supersede the historical 60-, 93- and 133-assertion fixtures.

High-level cycles retain live same-process clients through each authority gap,
then explicitly reset and rejoin them with fresh admission after restoring the
physics checkpoint. The matrix qualifies 18 live-client fault recoveries and
24 fresh admissions, including initial joins. Connected low-level clients now
add another 18 recoveries and 24 admissions in the same-process fixtures. Their
checks cover native disconnection, cleared peers/entities, retired-handle
rejection, exact opaque baseline bytes and bidirectional application/channel
delivery. Raw transport ownership metadata does not authorize gameplay messages.

Six additional independent authority/client process pairs qualify 18 server
clock faults/native client disconnects and 24 fresh admissions on local Windows.
Clients keep polling during the authority gap, discover disconnection and rejoin
under a test-only trusted token refresh policy. Restored Box3D baselines, fresh
ownership and one owner input per admission are checked. The complete language
validator passes 27 steps in editor/Debug/Release. Production admission/backoff
and recovery policy, independent-process low-level faults, in-flight/concurrent reload,
process crashes and hard outages remain unqualified. See :doc:`language_testing`
for reproduction and the exact scope of each fixture.

The opt-in network/reload gate qualifies one local authority clock fault followed
by C++/C# debugger reload after both native sessions stop. Serialized dictionaries
retain native session references and method-name callbacks; explicit rebind and
fresh admission restore networking. The full repair gate and runtime-disabled
baseline pass with current fixture sources. This is Windows Debug editor-run
evidence, distinct from the 197-assertion editor/export language checks.
The separate live-reload gate keeps the same local authenticated pair connected
across managed/native compiler failures and C#, C++ and combined reloads. Six
checkpoints retain session identities, peer/entity handles and exact callback
counts, with both outbound simulators configured at 30 ms latency, 5 ms jitter
and 5 percent loss. This configuration does not measure actual packet drops or
WAN performance. In-flight/concurrent reload, arbitrary managed facade/event
closure persistence, automatic client physics rollback and exported-runtime reload
remain unqualified. See :doc:`hot_reload` for both modes and their exact scopes.

The optional ``--network-physics`` extension qualifies one explicit Box3D body
through those reload modes. GDScript drives a 60 Hz authority-clock stepper and
fixture-owned baseline codec; reconstructed C++/C# objects retain the native world
reference and agree on its body state. Live reload advances the same world/body
without new admission. Stopped recovery retains an exact trusted checkpoint,
transactionally rejects damaged bytes, explicitly restores the saved state and
resumes physics with a checkpoint-to-network clock offset after fresh admission.
The full physics/facade live/stopped gates pass, with fresh low-level physics live
and runtime-default regressions at the current source. The focused suite now
passes 293 semantic tests and fifteen invalid CLI cases.
This local Windows Debug editor-run evidence covers one authority/client pair
and one body. It does not establish automatic client rollback, general game/ABI
state persistence, production checkpoint policy or larger-world behavior.

The public low-level C# ``NetSession`` now supports explicit ownership transfer
through ``DetachForReload()`` and ``ResumeAfterReload(Dictionary)``. Applications
save the local capsule in serialization hooks and resubscribe their handlers.
The low-level live/stopped repair gates each perform 23 managed checks and retain
constant connection counts for all seven native signals, without stale delegate
or script errors. Changed helper sources also pass fresh 27-stage language
validation and 197 assertions each in editor/Debug/Release. The capsule transfers
low-level ownership only; arbitrary captured event closures remain unqualified.
See :doc:`hot_reload` for the same-thread and capsule contract.

High-level C# ``NetNode`` now preserves forwarding on its codec child through
serialization and reconnects its eleven signals without duplicate subscriptions.
Owners preserve the node reference in an exported property, resubscribe ordinary
application events and register named Godot message handlers. Derived serialization
overrides must call base. Full live/stopped node fixtures check owned inputs,
exact messages/raw packets and fresh recovery. Tree exit closes the session and
disconnects forwarding; current fixtures each pass three fresh-session traffic
cycles after reentry. Each retired native session has zero callbacks, each fresh
native signal has one, and all eleven typed forwards remain connected exactly once.
Eighteen managed checks per fixture verify close/stop state-callback replacement;
six checks cover freed codec replacement and polling policy. Reconfigure options
before fresh host/join and scope saved handles to their issuing session identity.
Local stale signal injection checks lifetime isolation, not WAN security.
Generic assembly/unload/ABI repair occurs before authenticated node traffic;
those failures during such traffic remain open. High-level C++ and physics-adapter
ownership, arbitrary game/closure state and broader reload/platform/scale/performance
acceptance remain separate work.

Changed shared-codec inputs also pass fresh 27-stage language builds with 197
assertions each in editor/Debug/Release, 72 admission cases, seven physics/network
lab cases and the updated default GDScript sample. Stop retains the configured
native session and callbacks; Close disconnects all seven callbacks and releases
it. Registered handlers remain on the codec. Arbitrary in-flight lifecycle mutation
and production admission/checkpoint policies remain unqualified.

Admission testing separates listener timestamp protection from key rotation.
The controlled native/GDScript matrix covers retained zero/nonzero test keys
and generated keys, same/cross-second token creation, and clock-failure/graceful
restart. It passed 24 cases each in the Windows editor and fresh Debug/Release
exports. Retained keys admit unused same-second tokens; older tokens fail the
listener's start-time gate. Generated keys reject both timings.

The earlier all-zero-key diagnostic is resolved within this controlled scope.
Historical probes lacked the timestamps needed to distinguish those causes;
they do not establish retrospective or general backend revocation guarantees.
See :doc:`admission_testing` and the integration record for exact evidence.

The generated ``source_manifest.json`` records the engine revision and source
hashes used by this documentation. Runtime evidence and outstanding acceptance
items are maintained in the `engine integration record
<https://github.com/ZSG-Studios/EGP/blob/master/doc/egp_integration_loop.md>`__.
Consult that record for exact binary identities and current results.

Inherited Godot tutorials describe common editor and gameplay concepts.
Follow :doc:`migration` and EGP's class reference for changed systems.
