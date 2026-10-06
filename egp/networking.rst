.. _doc_egp_networking:

Networking with Yojimbo
=======================

EGP builds Yojimbo into the engine. ``EGPNetSession`` exposes transport,
encrypted admission, raw channels and opaque entity replication. The installed
``EGPNet`` helper adds named messages, validated Dictionary states, ownership,
interest filtering and registered scene factories.

The C# ``EGP.Networking.NetNode`` and C++ ``egp::networking::Net`` facades use
the same GDScript codec and adapters. Install the helpers as described in
:doc:`getting_started`; C# also needs matching Mono builds and assemblies.

Starting a server
-----------------

Add a network node to the game's scene and configure it before hosting.
Check every returned error and use the same protocol, simulation fingerprint
and fixed tick rate at both endpoints.

.. tabs::

   .. code-tab:: gdscript GDScript

      var net := EGPNet.new()

      func _ready() -> void:
          add_child(net)
          var error := net.configure({"game_protocol": "my-game-v1"})
          if error == OK:
              error = net.host(10515)
          if error != OK:
              push_error("Network startup failed: %s" % error_string(error))

   .. code-tab:: csharp C#

      using EGP.Networking;
      using Godot;

      public partial class Game : Node
      {
          private readonly NetNode net = new();

          public override void _Ready()
          {
              AddChild(net);
              Error error = net.Configure(new NetOptions { GameProtocol = "my-game-v1" });
              if (error == Error.Ok)
                  error = net.Host(10515);
              if (error != Error.Ok)
                  GD.PushError($"Network startup failed: {error}");
          }
      }

   .. code-tab:: cpp C++

      #include "egp_net.hpp"

      // Keep this wrapper as a member for the lifetime of the game node.
      egp::networking::Net net(*game_node);
      egp::networking::Options options;
      options.game_protocol = "my-game-v1";
      godot::Error error = net.configure(options);
      if (error == godot::OK) {
          error = net.host(10515);
      }
      // Report error through the game's diagnostics when error != godot::OK.

Secure client admission
-----------------------

After the game's backend authenticates an account, the server issues a token:

.. code-block:: gdscript

   var admission := net.issue_token(player_id, "203.0.113.10:10515")
   if admission.get("error", FAILED) == OK:
       # Deliver admission.token to that authenticated player through your backend.
       pass

``203.0.113.10`` is an example address; replace it with the server's reachable
literal IPv4/IPv6 endpoint. Resolve hostnames in the trusted backend. The client
configures matching options and calls ``join_token(player_id, token)``. A
successful return starts the attempt; wait for ``Connected`` while polling.
For IPv6, also select an IPv6 local bind address, such as ``"::"``.

Tokens expire after 30 seconds by default. Authentication, matchmaking and
token delivery belong to the game/backend. Keep token bytes and private server
keys out of logs. Direct ``join()`` connections are restricted to literal
loopback addresses with ``allow_insecure_loopback=true`` on both endpoints.

Messages and authoritative state
--------------------------------

Register message names and allowed senders explicitly. A handler receives
``(peer_id, arguments)``; message names do not invoke arbitrary scene methods.

.. code-block:: gdscript

   # Server: accept a client request under a registered contract.
   net.register_message(&"chat", _on_chat, EGPNet.Sender.CLIENT)

   func _on_chat(peer_id: int, arguments: Array) -> void:
       # Validate size, types, permissions and gameplay values before applying them.
       pass

   # Client: server is always peer 0; check the returned Error.
   # var error := net.send_message(0, &"chat", ["Hello"])

Only the server may spawn, update or despawn replicated entities. ``spawn()``
returns ``0`` on failure. States reject serialized objects and have a 4096-byte
wire limit. Connection ownership controls input dispatch; gameplay must still
validate the input values. Use registered scene factories for presentation.

Replication sends changed revisions as bounded complete states. Updates made
while an entity's state awaits acknowledgment are coalesced. Intermediate
revisions may be skipped; use application messages for events that must each
arrive. Four raw user channels support reliable ordered messages up to 4096
bytes and unreliable unordered messages up to 900 bytes.

Polling, budgets and recovery
-----------------------------

All session operations and disposal run on the constructing Godot thread.
The helper polls automatically unless ``auto_poll`` is disabled. Do not poll
the same session from another thread or a second clock.

Per-peer outgoing quota exhaustion returns ``ERR_BUSY``. Valid incoming bursts
wait in bounded queues, with channels advancing in rounds. Byte charges estimate
payload and metadata; they do not cap transport wire bandwidth or all decoding
work. Check send errors, including partial broadcast admission.

A poll executes at most eight fixed ticks. More than 0.5 seconds of accumulated
simulation time stops the endpoint, clears entities/ticks and returns ``FAILED``.
Client simulation time starts after the authoritative baseline completes and
the session becomes ``Connected``; transport time spent connecting or
synchronizing does not consume that active simulation budget.
After polling returns, close/reconfigure the facade, obtain fresh admission and
receive a new authoritative baseline. Recovery must not occur synchronously
inside a poll callback. Revoke old ownership and grant it to the new connection.

See :doc:`prediction` for bounded replay and :doc:`network_lab` for dedicated
servers, listen hosts, impairment, repeated client stalls and server replacement.
The complete configuration, commands and result schemas are in
:doc:`networking_reference` and :ref:`EGPNetSession <class_EGPNetSession>`.
