.. _doc_egp_explicit_world:

Explicit Box3D worlds
=====================

``EGPBox3DWorld`` owns a fixed-tick simulation independent of SceneTree physics.
Use ordinary scene nodes for scene physics; use this class when the application
needs stable entity IDs, ordered commands and trusted local solver snapshots.

Creating and stepping bodies
----------------------------

These examples create a static floor and a dynamic sphere, then advance one
tick. The C# generated native class is named ``Godot.EgpBox3DWorld``; C++ uses
``godot::EGPBox3DWorld`` from the matching embedded SDK.

.. tabs::

   .. code-tab:: gdscript GDScript

      extends Node

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

   .. code-tab:: csharp C#

      using Godot;

      public partial class PhysicsWorldExample : Node
      {
          public EgpBox3DWorld World { get; } = new();

          public Error CreateWorld()
          {
              Error error = World.Configure(60, 4, 1, new Vector3(0, -9.8f, 0));
              if (error != Error.Ok) return error;
              error = World.QueueCreateBox(1, 0, new Vector3(0, -1, 0),
                  new Vector3(10, 1, 10), 0);
              if (error != Error.Ok) return error;
              error = World.QueueCreateSphere(2, 0, new Vector3(0, 3, 0), 0.5);
              if (error != Error.Ok)
              {
                  World.ClearPendingCommands();
                  return error;
              }
              return World.StepTick(World.GetTick() + 1);
          }
      }

   .. code-tab:: cpp C++

      #include <godot_cpp/classes/egp_box3d_world.hpp>

      godot::Error create_world(godot::Ref<godot::EGPBox3DWorld> &world) {
          world.instantiate();
          godot::Error error = world->configure(60, 4, 1, godot::Vector3(0, -9.8, 0));
          if (error != godot::OK) return error;
          error = world->queue_create_box(1, 0, godot::Vector3(0, -1, 0),
              godot::Vector3(10, 1, 10), 0);
          if (error != godot::OK) return error;
          error = world->queue_create_sphere(2, 0, godot::Vector3(0, 3, 0), 0.5);
          if (error != godot::OK) {
              world->clear_pending_commands();
              return error;
          }
          return world->step_tick(world->get_tick() + 1);
      }

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

Keep checkpoint bytes in trusted local history and check the returned restore
error:

.. tabs::

   .. code-tab:: gdscript GDScript

      func restore_local_checkpoint(world: EGPBox3DWorld,
              checkpoint: PackedByteArray) -> Error:
          if checkpoint.is_empty():
              return ERR_INVALID_DATA
          return world.restore_snapshot(checkpoint)

      # At a command-free boundary:
      # var checkpoint := world.capture_snapshot()

   .. code-tab:: csharp C#

      using Godot;

      public static class LocalCheckpoint
      {
          public static Error Restore(EgpBox3DWorld world, byte[] checkpoint)
          {
              if (checkpoint.Length == 0) return Error.InvalidData;
              return world.RestoreSnapshot(checkpoint);
          }
      }

      // At a command-free boundary:
      // byte[] checkpoint = world.CaptureSnapshot();

   .. code-tab:: cpp C++

      #include <godot_cpp/classes/egp_box3d_world.hpp>

      godot::Error restore_local_checkpoint(
              const godot::Ref<godot::EGPBox3DWorld> &world,
              const godot::PackedByteArray &checkpoint) {
          if (checkpoint.is_empty()) return godot::ERR_INVALID_DATA;
          return world->restore_snapshot(checkpoint);
      }

      // At a command-free boundary:
      // godot::PackedByteArray checkpoint = world->capture_snapshot();

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

Stable body mapping
-------------------

``track(entity, body_id=0)`` maps a live server-owned network entity to a world
body. C# uses ``Track(entity, bodyId=0)``; C++ uses
``track(entity, body_id=0)``. Omitting the second argument, or passing zero,
keeps the original convention of using the network entity ID as the body ID.
Negative body IDs return ``ERR_INVALID_PARAMETER``. Explicit positive IDs let
a new network handle replicate the same restored body after fresh admission.

The body must exist in the configured world. Tracking requires an attached
adapter, server mode and a live network entity; missing body state is not
published. In these examples, body ``2`` is the sphere created above. Configure
the network with the world's fingerprint and tick rate before hosting, and
keep the adapter alive while it is attached.

.. tabs::

   .. code-tab:: gdscript GDScript

      var adapter := EGPNetBox3D.new()

      func map_body(net: EGPNet, world: EGPBox3DWorld, entity: int) -> Error:
          var error := adapter.attach(net, world)
          if error != OK:
              return error
          error = adapter.track(entity, 2)
          if error != OK:
              adapter.detach()
          return error

   .. code-tab:: csharp C#

      using EGP.Networking;
      using Godot;

      public static class StableBodyMapping
      {
          public static Error MapBody(NetBox3D adapter, NetNode net,
                  EgpBox3DWorld world, long entity)
          {
              Error error = adapter.Attach(net, world);
              if (error != Error.Ok) return error;
              error = adapter.Track(entity, 2);
              if (error != Error.Ok) adapter.Detach();
              return error;
          }
      }

      // Keep the adapter in the game's owner; Detach/Dispose before releasing it.

   .. code-tab:: cpp C++

      #include "egp_net.hpp"
      #include <godot_cpp/classes/egp_box3d_world.hpp>

      godot::Error map_body(egp::networking::Box3D &adapter,
              egp::networking::Net &net,
              const godot::Ref<godot::EGPBox3DWorld> &world, int64_t entity) {
          godot::Error error = adapter.attach(net, world);
          if (error != godot::OK) return error;
          error = adapter.track(entity, 2);
          if (error != godot::OK) adapter.detach();
          return error;
      }

      // Keep adapter as an owning game member; detach before destroying net.

During server recovery, detach the adapter before restoring the trusted local
checkpoint. Recreate network entities under fresh connection ownership, then
attach again and track their new handles against the preserved body IDs. The
restored world advances from its own tick even when the restarted transport
clock begins at zero. The opt-in ``--physics`` :doc:`network lab <network_lab>`
demonstrates bounded checkpoint restoration and six-tick local replay.

The separate ``--network-physics`` :doc:`reload fixture <hot_reload>` retains
one native world/body through live C#/C++ reload or explicit trusted checkpoint
restoration after a stopped authority fault. It uses a GDScript clock callback
and fixture-owned baseline codec. This bounded Windows Debug evidence is distinct
from automatic client rollback and general game-state persistence.

See :doc:`box3d`, :doc:`prediction` and the
:ref:`EGPBox3DWorld class reference <class_EGPBox3DWorld>`.
