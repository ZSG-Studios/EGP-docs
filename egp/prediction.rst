.. _doc_egp_prediction:

Prediction and reconciliation
=============================

Superposition deterministic prediction
--------------------------------------

:ref:`SuperpositionPrediction <class_SuperpositionPrediction>` is the native
prediction journal shared by GDScript, C# and C++. It predicts complete local
world inputs and reconciles authoritative input/hash frames. Corrections restore
a trusted snapshot captured locally and replay the affected ticks. Peers never
supply solver snapshots to restore.

Supply ``capture() -> PackedByteArray``, ``restore(local_snapshot) -> Error``,
``simulate(tick, input, replay) -> Error`` and ``state_hash() -> String`` callbacks.
The hash contains 16 hexadecimal digits. Simulation applies complete canonical
input and steps the world exactly once; suppress presentation effects in replay.

After matching genesis and simulation profiles, configure the journal and predict
consecutive ticks. Call ``accept(frames, epoch)`` with consecutive
``{tick, input, hash}`` dictionaries from the authority. Input differences trigger
replay. Hash mismatch or callback failure disables prediction and emits
``resync_required``. Establish fresh trusted local genesis, then defer
``reset(new_epoch, initial_tick)`` until the current callback completes.

.. tabs::

   .. code-tab:: gdscript GDScript

      var journal := SuperpositionPrediction.new()
      var error := journal.configure(capture, restore, simulate, state_hash)
      # Check each returned Error before advancing gameplay.
      error = journal.predict(tick, canonical_input)
      error = journal.accept(authoritative_frames, epoch)

   .. code-tab:: csharp C#

      using Godot;
      using Godot.Collections;

      using var journal = new SuperpositionPrediction();
      Error error = journal.Configure(capture, restore, simulate, stateHash);
      // Callbacks are Godot.Callable values; check each returned Error.
      error = journal.Predict(tick, canonicalInput);
      error = journal.Accept(authoritativeFrames, epoch);

   .. code-tab:: cpp C++

      #include <godot_cpp/classes/superposition_prediction.hpp>

      godot::Ref<godot::SuperpositionPrediction> journal;
      journal.instantiate();
      godot::Error error = journal->configure(capture, restore, simulate, state_hash);
      // Check each returned Error before advancing gameplay.
      error = journal->predict(tick, canonical_input);
      error = journal->accept(authoritative_frames, epoch);

Default bounds are 128 pending ticks, 1 MiB per snapshot and 32 MiB total history.
Maximums are 512 ticks and 64 MiB total. Capacity pressure refuses prediction
before invoking simulation. Epochs increase when the authority restores a
checkpoint or changes the simulation timeline. Old frames cannot correct a new
epoch. Statistics expose history, corrections, replayed ticks and hash failures.
Methods belong to the creating thread and reject recursive mutations.

Inspector Box3D adapter
-----------------------

Install the helpers with ``python misc/scripts/install_egp_net_helpers.py
--project /path/to/game``, then attach
``addons/egp_net/egp_net_box3d_prediction.gd`` to a node. Set the explicit world
provider, predicted body and optional presentation paths. The default World
Provider and Hook Node paths both select the parent (``..``). The provider must
expose the local ``EGPBox3DWorld`` through the configured World Property, which
defaults to ``world``. A parent
:ref:`SuperpositionWorld <class_SuperpositionWorld>` provides the session
automatically; create and supply the Box3D world separately. The adapter
delegates its history to the native journal.

Implement ``input_for_tick(tick) -> PackedByteArray`` and
``apply_input(world, tick, input, replay) -> Error``. The latter queues commands;
the adapter owns the fixed step. Its standard six-byte schema contains two
signed axes and a 16-bit button mask. Custom fixed-size schemas require a
validation callback. The server validates identity, input bounds and tick
windows, chooses canonical world input and publishes input/hash frames.

All interacting bodies, lifecycle events, random state and relevant gameplay
must share the same deterministic state/input contract. Predicting one body
against a different collision world cannot guarantee matching hashes. Reconnects
and history expiry require fresh trusted genesis. See :doc:`superposition` for
the session, spawning and RPC workflow.

Snapshot-state prediction helper
--------------------------------

``EGPNetPrediction`` stores bounded local input/state history and replays it
after an authoritative correction. C# ``NetPrediction`` and C++ ``Prediction``
execute the same implementation. The game supplies complete state capture,
restore and simulation callbacks.

Callback contract
-----------------

* ``capture()`` returns a nonempty ``PackedByteArray`` containing complete local
  predicted state.
* ``restore(state)`` returns an ``Error`` after restoring that state.
* ``simulate(tick, input, replay)`` returns an ``Error``; suppress duplicate audio,
  particles and other presentation effects when ``replay`` is true.

Call ``configure(capture, restore, simulate, initial_tick)`` once, then
``predict(tick, input)`` with consecutive ticks. Send the same tick/input
through the game's ownership-checked input contract. The server decides how
late or rejected input affects acknowledgment; the transport does not define
the gameplay policy.

Call ``reconcile(acknowledged_tick, authoritative_state)`` when the server
acknowledges an accepted input boundary. When local and authoritative state
differ, the helper restores that boundary and replays remaining inputs.
Old acknowledgments are ignored. Invalid state/callback failures require an
explicit baseline reset; listen for ``resync_required``.

Using the helper
----------------

These controllers accept the game's capture/restore/simulate callbacks and
expose the same configure, predict and reconciliation sequence. The callbacks
must implement the complete state contract above. In C++, supply Godot
``Callable`` objects bound to registered game methods; C# delegates are adapted
to the shared GDScript implementation.

.. tabs::

   .. code-tab:: gdscript GDScript

      extends Node

      var prediction := EGPNetPrediction.new()

      func start_prediction(capture: Callable, restore: Callable,
              simulate: Callable, initial_tick: int = 0) -> Error:
          return prediction.configure(capture, restore, simulate, initial_tick)

      func predict_input(tick: int, input: PackedByteArray) -> Error:
          return prediction.predict(tick, input)

      func accept_authority(tick: int, state: PackedByteArray) -> Error:
          return prediction.reconcile(tick, state)

   .. code-tab:: csharp C#

      using System;
      using EGP.Networking;
      using Godot;

      public sealed class PredictionController : IDisposable
      {
          private readonly NetPrediction prediction = new();

          public Error StartPrediction(Func<byte[]> capture,
                  Func<byte[], Error> restore,
                  Func<long, byte[], bool, Error> simulate, long initialTick = 0)
              => prediction.Configure(capture, restore, simulate, initialTick);

          public Error PredictInput(long tick, byte[] input)
              => prediction.Predict(tick, input);

          public Error AcceptAuthority(long tick, byte[] state)
              => prediction.Reconcile(tick, state);

          public void Dispose() => prediction.Dispose();
      }

   .. code-tab:: cpp C++

      #include "egp_net.hpp"

      class PredictionController {
          egp::networking::Prediction prediction;
      public:
          godot::Error start_prediction(const godot::Callable &capture,
                  const godot::Callable &restore, const godot::Callable &simulate,
                  int64_t initial_tick = 0) {
              return prediction.configure(capture, restore, simulate, initial_tick);
          }
          godot::Error predict_input(int64_t tick, const godot::PackedByteArray &input) {
              return prediction.predict(tick, input);
          }
          godot::Error accept_authority(int64_t tick, const godot::PackedByteArray &state) {
              return prediction.reconcile(tick, state);
          }
      };

Check every returned error at the game call site. Prediction failures can
require a fresh baseline; a successful enqueue/send is not an input
acknowledgment. Dispose the C# controller only when it will no longer be used,
and keep C++ wrappers alive for the callbacks' lifetime.

Limits
------

Defaults are 128 pending ticks, 64 KiB per local snapshot and 8 MiB of history.
History pressure returns ``ERR_BUSY`` before a new prediction rather than
silently discarding inputs. Local limits are independent of the 4096-byte
network state limit. A larger local snapshot needs a separate bounded
authoritative wire-state design.

An explicit Box3D world can supply trusted local solver snapshots, but complete
game state includes authoritative lifecycle, gameplay data and application
acknowledgments too. Lag-compensated hit tests and collision correction
convergence remain separate gameplay integration work. The native deterministic
journal supports complete-world replay with matching genesis and canonical input.

See :doc:`explicit_world`, :doc:`helper_reference` and :doc:`networking_reference`.
