.. _doc_egp_migration:

Migrating from Godot
====================

Back up the project and use a separate working copy for migration. EGP follows
Godot's development branch, so check both upstream version changes and the
fork-specific changes below. Keep the editor, templates and generated APIs matched.

Rendering
---------

Rendered EGP projects use Forward+ through a supported RenderingDevice driver.
Set ``rendering/renderer/rendering_method`` and its mobile override to
``forward_plus``. Compatibility and Mobile renderers, OpenGL/OpenGL ES and
ANGLE are removed; old renderer selections are rejected and unsupported
devices have no fallback renderer.

Recheck imported materials, lighting and render settings on the target GPU.
Browser exports and WebXR are unsupported. Headless servers and tooling retain
the dummy backend through ``--headless``. See :ref:`doc_renderers` for details.

Physics
-------

Box2D is the sole native 2D backend and Box3D the sole native 3D backend.
Old backend selections are migrated at startup. Ordinary physics nodes and
``PhysicsServer2D/3D`` remain the scene-facing APIs, but solver behavior and
supported parameters differ. Changing the backend does not establish full parity.

* Review :doc:`box2d` for fixed-rate configuration, convex polygon limits,
  unsupported infinite boundaries/separation rays and CCD changes.
* Review :doc:`box3d` for shape, query, character and joint compatibility.
* Recheck joint parameter names in the generated class reference. EGP exposes
  native configuration and removes obsolete Godot/Jolt solver controls.
* ``SeparationRayShape3D`` is removed. Adapt motion queries to the supported
  shape-query APIs rather than copying inherited separation-ray examples.
* Explicit ``EGPBox3DWorld`` snapshots do not restore SceneTree physics bodies.

Multiplayer
-----------

EGP replaces Godot's high-level scene multiplayer with Yojimbo. Inherited
``MultiplayerAPI``, ``SceneMultiplayer``, ``MultiplayerPeer``, multiplayer
spawners/synchronizers, ENet/WebRTC multiplayer peers and ``@rpc`` examples
are not EGP networking APIs.

.. list-table:: Migration map
   :header-rows: 1
   :widths: 35 65

   * - Existing approach
     - EGP integration
   * - Create an ENet multiplayer server/client
     - Configure ``EGPNet``; use ``host()`` and encrypted ``join_token()`` admission.
   * - Invoke scene-node RPC methods
     - Register named message contracts with ``register_message()`` and use ``send_message()``.
   * - Automatically replicate scene properties
     - Publish bounded authoritative entity states with ``spawn()`` and ``update_entity()``.
   * - Automatically spawn replicated nodes
     - Register scene factories explicitly and select a kind for each entity.
   * - Persist node authority across reconnect
     - Assign ownership to the current connection generation's ``peer_id``.
   * - Rely on transport reconnection/persistence
     - Obtain fresh admission, rebuild ownership and restore application state explicitly.

Account ``client_id``, connection ``peer_id`` and replicated ``entity`` handles
have separate lifetimes. A client addresses the server as peer ``0``.
Clients never receive the server's private admission key.

Low-level HTTP, TCP, UDP and WebSocket utilities are separate from the
multiplayer transport. Their availability depends on the build. EGP's desktop
Yojimbo transport does not establish browser multiplayer support.

See :doc:`networking`, :doc:`networking_reference` and :doc:`network_lab`.

Bindings and runtime reload
---------------------------

Rebuild extensions against the SDK extracted by the intended EGP editor.
Regenerate C# glue from that same binary; stale packages can share the same
development version number. Inspect the API SHA256 when diagnosing mismatch.

Running-game reload requires ``debug/hot_reload/enable_runtime=true`` before
launching an editor-run game. Export templates disable it. Compatible reload
can preserve instances and state; native hierarchy/ABI changes may require a
restart. See :doc:`hot_reload` and :doc:`api_contract`.
