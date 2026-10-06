.. _doc_egp_explicit_world:

Explicit Box3D worlds
=====================

``EGPBox3DWorld`` owns a fixed-tick simulation independent of SceneTree physics.
Use ordinary scene nodes for scene physics; use this class when the application
needs stable entity IDs, ordered commands and trusted local solver snapshots.

Creating and stepping bodies
----------------------------

.. code-block:: gdscript

   var world := EGPBox3DWorld.new()

   func create_world() -> Error:
       var error := world.configure(60, 4, 1, Vector3(0, -9.8, 0))
       if error != OK:
           return error
       error = world.queue_create_box(1, 0, Vector3(0, -1, 0), Vector3(10, 1, 10), 0)
       if error != OK:
           return error
       error = world.queue_create_sphere(2, 0, Vector3(0, 3, 0), 0.5)
       if error != OK:
           world.clear_pending_commands()
           return error
       return world.step_tick(world.get_tick() + 1)

Configuration is immutable. Bodies use meters and positive signed 64-bit
application IDs. Body types are ``0`` static, ``1`` kinematic and ``2`` dynamic.
Assign sequences authoritatively; commands execute in ``(entity_id, sequence)``
order. Assigning sequence numbers from packet arrival can break determinism.

``step_tick()`` requires the next consecutive tick and validates the complete
command batch before mutation. Clear a rejected batch before trying a repaired
one. ``apply_queued_commands()`` applies an ordered batch without advancing time.
Read position, rotation and velocities with ``get_body_state(entity_id)``.

Snapshots and correction
------------------------

Capture snapshots at a boundary with no queued commands. Snapshots include
hidden local solver state and are bounded to 64 MiB. Restore only trusted
local history on a compatible binary/ABI. They are not network packets or a
portable save format; a checksum does not authenticate hostile input.

For a client correction, restore the snapshot associated with the accepted
input tick, apply authoritative lifecycle and pose/velocity commands, flush
those commands, capture the boundary and replay buffered input ticks.
Pose/velocity correction alone does not reconstruct remote contact caches.

The 16-character ``get_state_hash()`` is diagnostic and excludes some latent
solver state. Compare it only at matching ticks, profiles and topology.
Matching fingerprints alone do not prove cross-platform determinism.

Networking clock
----------------

Configure the world first and use ``get_simulation_fingerprint()`` in the
network options. ``EGPNetBox3D.attach(net, world)`` checks the fingerprint and
tick rate, steps on server simulation ticks and publishes tracked body states.
Detach the adapter before freeing the network node. Never step that world from
both SceneTree and networking clocks. This adapter does not implement client rollback.

See :doc:`box3d`, :doc:`prediction` and the
:ref:`EGPBox3DWorld class reference <class_EGPBox3DWorld>`.
