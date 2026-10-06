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
