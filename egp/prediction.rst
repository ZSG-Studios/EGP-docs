.. _doc_egp_prediction:

Prediction and reconciliation
=============================

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
acknowledgments too. Scene-level physics rollback, lag-compensated hit tests and
collision correction convergence remain separate integration work.

See :doc:`explicit_world`, :doc:`helper_reference` and :doc:`networking_reference`.
