.. _doc_egp_qualification:

Support and qualification
=========================

EGP is a development fork based on Godot 4.8-dev. The source implements the
systems below; qualification applies to the binaries, platforms and fixtures
identified in the engine's receipts. Build success and API exposure alone do
not establish runtime behavior or production readiness.

Published upstream consolidation
--------------------------------

The documentation is generated from engine revision
``745f2496d364eb4a3495abf949610ecda51e58b1``. It includes the sixteen incoming
official Godot commits through ``3ea0cf3e72699c5e3b35f7956670ac93b9d1d4a0``.
This is a pinned upstream snapshot; later upstream commits require another
compatibility review.

The Windows Mono editor was compiled from
``7b57a3b3140cb1c8b0bbcfb6bbe2c1f4eab70161``. Debug and Release templates were
compiled from ``c6a6920685b844ff0ba30d2e794117b776edf72a``; the later export fix
affects the editor only. Later source changes include the compile-time zstd
guard and repairs to test registration, optional-physics CSG compilation,
Box2D adapter contracts, Clang floating-point settings, SCU generation and
platform compiler warnings. CSG mesh updates remain scheduled when physics is
disabled. These installed
binaries were not rebuilt for those later changes. Actual MSVC zstd probes
accept the pinned header and an absent macro, and reject an incorrect value;
a complete engine using system zstd remains unqualified. The published source
pin and compiled artifact pins therefore differ.

The combined gate records 29 passing scopes against those Windows artifacts,
including language, physics,
reload, network-lab and admission regressions. Native Debug/Release suites pass
120 checks and ten CTest tests each. The captured extension API remains
byte-identical, with matching SDK key ``4bc13481314e7023`` and MSVC 19.51 libraries.
New native and managed artifacts supersede the previous binary identities.
Consult the `pinned integration record
<https://github.com/ZSG-Studios/EGP/blob/745f2496d364eb4a3495abf949610ecda51e58b1/doc/egp_integration_loop.md>`__
for exact hashes, commands and retained failed controls.

The subsequent C++ helper update adds explicit ``Net``/``Box3D`` ownership
handoff without rebuilding those 95 installed artifacts or changing the ABI.
Two actual compatible Debug DLL reloads pass 60 capsule checks and 138 runtime
assertions with retained authenticated local sessions, world/body identities,
exact solver state during unload and callback/handler resubscription. Final
helper inputs also pass the 27-stage editor/Debug/Release language matrix.
Applications pause manual polling at a Godot-thread safe boundary. Automatic or
in-flight transfer, prolonged failed-library ownership recovery and exported-game
reload remain open. A separate missing/invalid-DLL fixture passes four failed
loads and two compatible repairs with 158 assertions, at observed 25 ms and
14 ms fault intervals while polling is paused. See
:ref:`the C++ handoff contract <doc_egp_cpp_owner_handoff>`.

Inherited scene references in binary exports
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When an inherited scene introduces a child referenced by a base scene property,
binary scene conversion must retain that property's serialized NodePath until
the complete scene is instantiated. Unmodified conversion now saves the
original PackedScene. Export plugins that modify the scene still cause it to be
instantiated and repacked, preserving their changes.

The focused fixture passes 36 assertions in the editor and each relocated
Debug/Release game: 108 total. Six plain, inherited and three-level scenes cover
GDScript Node and C# NetNode references in scalar, array and dictionary
key/value properties. Six separate checks verify plugin-added metadata and
renamed children in relocated binary exports. These checks do not establish
every combination of customized inherited scenes.

Run from the engine checkout using matching Mono packages and templates:

.. code-block:: powershell

   python misc/scripts/validate_egp_scene_node_refs.py `
       --engine bin/godot.windows.editor.dev.x86_64.mono.exe `
       --packages bin/GodotSharp/Tools/nupkgs `
       --debug-template bin/godot.windows.template_debug.x86_64.mono.exe `
       --release-template bin/godot.windows.template_release.x86_64.mono.exe `
       --output .build/scene-references-new

   python misc/scripts/validate_egp_export_customization.py `
       --editor bin/godot.windows.editor.dev.x86_64.mono.exe `
       --debug-template bin/godot.windows.template_debug.x86_64.mono.exe `
       --release-template bin/godot.windows.template_release.x86_64.mono.exe `
       --output .build/export-customization-new

Use fresh output directories. The scene validator rejects export error output
even if the exporter exits zero, creates its managed solution and verifies the
relocated games. The trilingual sample now tracks its required
``NetInterop.sln`` so fresh checkouts do not depend on an ignored local file.

Source checkout verification
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Vendor source verification accepts the original raw hashes or explicit UTF-8/LF
pins for Git line-ending conversion. It rejects other content changes; seven
semantic checks and a changed-content control qualify that bounded behavior.
Vendor-only validation does not establish native or runtime compatibility:

.. code-block:: console

   python misc/scripts/validate_egp_net.py --verify-vendor-only --output .build/vendor-identity-new

Native test cadence across platforms
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The delayed-packet fixture pumps at 10 ms intervals so its configured
1.0-second latency and 0.6-second jitter fit within the simulator's 512 packet
slots. The earlier 2 ms cadence can overwrite occupied slots on Linux despite
zero configured random loss. A frozen Linux baseline reproduces the failure;
three candidate runs deliver all 128 packets with zero rejection. The
12-second deadline and delivery, quota, ordering, fragmentation and wire-rejection
assertions remain unchanged.

Full local native suites pass 120 checks and all ten CTest cases in Windows
MSVC Debug/Release and Ubuntu WSL/GCC Debug. Final formatted-fixture tests also
pass in Windows Debug and Linux Debug. This fixture correction changes no
engine/core/vendor implementation or installed artifact. It qualifies these
native tests, rather than complete Linux editors, exports, WAN behavior or
overload performance. Hosted results remain separately identified in the
pinned integration record.

The `hosted networking run at revision 745f2496d3
<https://github.com/ZSG-Studios/EGP/actions/runs/37546566363>`__ passes on
Windows, Linux and macOS in Debug: 120 native checks and all eleven CTest
cases per platform. The added abrupt-disconnect fixture drops the original
owner's heartbeat and disconnect notification. It separately checks transport
timeout detection, immediate server authority revocation and delivery to the
remaining client within the existing five-second replication deadline. Two
reconnect cycles retain the 64-entity load and 32-message-per-second budget.
The original compound deadline fails the retained abrupt-outage control.
This hosted result does not qualify Release, WAN behavior or complete engine
and managed runtime coverage.

Strict compilation and CI profiles
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The engine test runner now requires the configured physics backends instead of
falling back to removed dummy servers. Standalone Box3D executables retain their
own CMake/CTest targets and are excluded from the engine's doctest source list.
The viewport test bodies and their existing assertions remain present.

The hosted Windows editor built from ``0a2186345`` passes all 1,414 unit test
cases and 423,722 assertions with test inputs pinned to ``b6227eebab``; three
cases remain skipped by the runner. The full GDScript text fixture suite passes,
and the original retired-RPC fixture fails against the same binary. The optional
binary-token fixture mode remains unqualified. These checks do not replace the
latest full platform matrix or managed and graphical runtime validation.

The API compatibility script passes all eight official reference versions from
4.0 through 4.7 against that editor. Exact documented exceptions cover EGP's
intentional networking and physics API changes. Unlisted removals, signatures
and hashes remain failures; retained methods remain in the native lookup test.

The compiled editor's doctool output also matches the synchronized class XML,
including four concrete Box2D/Box3D backend classes. This verifies reference
metadata for that compiled profile.

Matching Linux Mono Debug and Release templates from ``0a2186345`` run a pack
exported by the Windows editor from the same revision. A headless smoke test
advances a CircleShape2D/RigidBody2D and a SphereShape3D/RigidBody3D under gravity
for 60 physics ticks, verifies finite positions and confirms EGPNetSession is
exposed. This primitive physics smoke test does not qualify networking traffic,
managed scripts, hot reload, graphical behavior or larger worlds.

Current Linux Mono Debug and Release templates at ``745f2496d3`` also pass
headless probes using a pack exported by the matching Windows native editor.
The physics probe checks the actual Box2D and Box3D backend types and advances
both primitive bodies for 60 ticks. Additional GDScript fixtures pass encrypted
admission, prediction/replay, lifecycle and separate dedicated-server/client
process checks in both templates. Matching Windows editor fixtures also pass.
These checks cover GDScript running in Mono templates; they do not exercise
C# scripts, graphical rendering, hot reload or production networking scale.

All 26 Box2D adapter translation units compile under optimized GCC and Clang
with warnings treated as errors. The cleanup preserves signed index rejection,
orders and initializes members correctly, and follows the upstream query-result
contract: collider IDs resolve live objects through the current getter.
All 31 Box3D adapter translation units also pass strict GCC and Clang compilation.
CSG's path update compiles both with and without physics; these focused compiler
checks establish neither a full engine link nor mobile runtime behavior.

Clang-cl uses explicit safe floating-point options with contraction disabled,
avoiding the conflicting precise-model/FMA override. The failing driver control
is retained, and optimized LLVM IR keeps separate multiply/add operations even
when the CPU supports FMA. Both standalone Box3D deterministic replay and joint
tests pass under Windows Clang-cl Release with warnings treated as errors.
Full engine builds and runtime qualification remain separately identified in
the integration record.

The `native C++ workflow
<https://github.com/ZSG-Studios/EGP/actions/runs/37528340019>`__ passes on
Windows x86_64, Linux x86_64 and macOS arm64 at source revision
``2b7e76be942716a21c139e00036468965731ddfd``. Its 39 CLI, native-game and
export checks have the expected exit codes; twelve game logs report success,
and the SDK unit tests pass. These headless, non-Mono checks qualify that
earlier source revision. They do not establish graphical behavior, managed
integration, hot reload or completion of the latest full engine matrix.

System support
--------------

Box2D and Box3D currently build on single-precision x86_64/arm64 desktop targets.
The inherited CI matrix uses explicit no-physics export profiles for Android,
iOS, Web and double precision. Desktop editors retain physics; Android and
double-precision editors are unsupported. The double-precision sanitizer
template retains unit tests, and the regression project's import, rendering and
runtime checks run in the single-precision Clang sanitizer editor. SCU and GCC
sanitizer coverage use a separate single-precision desktop editor, while the
double-precision template builds without SCU. A successful
export-profile build would establish compilation for its selected capabilities;
it would not qualify mobile physics or games that require omitted physics nodes.

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
passes 662 semantic tests and eighteen invalid CLI cases.
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
those failures during such traffic remain open. Automatic C++ ownership
transfer, arbitrary game/closure state and broader reload/platform/scale/performance
acceptance remain separate work.

Changed shared-codec inputs also pass fresh 27-stage language builds with 197
assertions each in editor/Debug/Release, 72 admission cases, seven physics/network
lab cases and the updated default GDScript sample. Stop retains the configured
native session and callbacks; Close disconnects all seven callbacks and releases
it. Registered handlers remain on the codec. Arbitrary in-flight lifecycle mutation
and production admission/checkpoint policies remain unqualified.

Public C# ``NetBox3D`` ownership now transfers the existing adapter, world and
stable body map across reload with explicit application event resubscription.
Fresh live/stopped fixtures cover 22 capsule checks each, exact three-signal
counts, before/after events for each completed tick, tree exit/reentry and three
fresh-session cycles. New entities remap to retained body 10000 and client physics
advances. Debugger commands defer until the active poll/tick returns; preserved
failing controls do not qualify arbitrary synchronous callback mutation. Fresh
27-stage editor/Debug/Release language builds and low-facade/default runtime
regressions pass. The upstream consolidation repeats the GDS-only lab/admission
matrix against the updated Windows artifacts. See
:doc:`hot_reload` for ownership, disposal, command and scope details.

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
