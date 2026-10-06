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

Fresh C#/C++ fixtures pass 133 interoperability assertions each in the Windows
Mono editor and relocated Debug/Release exports. They include three successive
clock failures per language on both high-level and low-level sessions: 36 local
faults across those configurations. Each cycle checks the native failure,
retained session/port, retired handles and explicit recovery. High-level fixtures
also restore trusted local Box3D checkpoints and map fresh entities to stable
bodies. These results supersede the historical 60- and 93-assertion fixtures.

High-level cycles retain live same-process clients through each authority gap,
then explicitly reset and rejoin them with fresh admission after restoring the
physics checkpoint. The matrix qualifies 18 live-client fault recoveries and
24 fresh admissions, including initial joins. Low-level cycles still have no
peers. Automatic recovery, independent-process stalled servers, connected
low-level faults and hot reload during faults remain unqualified. See
:doc:`language_testing` for reproduction, evidence and the distinction from
separate-process networking.

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
