.. _doc_high_level_multiplayer:

.. _doc_high_level_multiplayer_rpcs:

High-level multiplayer in EGP
=============================

EGP uses Yojimbo with the ``EGPNetSession`` native class and installed
``EGPNet`` GDScript, C# and C++ helpers. Godot's scene RPC, ENet multiplayer,
automatic spawner and synchronizer APIs have been removed.

See :doc:`/egp/networking` for secure server/client setup, registered messages,
authoritative entity replication and connection-generation ownership.
See :doc:`/egp/migration` for the old-to-new API map and
:doc:`/egp/networking_reference` for all options, limits and lifecycle rules.

Use :doc:`/egp/network_lab` to run bounded dedicated-server/listen-host fixtures
with impairment, reconnect, server replacement and repeated client stalls.
