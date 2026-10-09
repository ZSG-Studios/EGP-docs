.. _doc_egp_helper_reference:

Superpos language API
=====================

GDScript, generated C# (``Godot.SuperposSession``) and generated godot-cpp
(``godot::SuperposSession``) call the same native ClassDB implementation.
Use the matching editor's generated bindings and C++17 extension SDK.
The independent core's C++23 headers are private engine implementation.

See :doc:`networking_reference` for API usage, checked counters, packet delivery,
owner retirement and qualification limits. See :doc:`superpos_migration` before
porting legacy helper users. Superpos does not install GDScript bridge helpers.

The old ``EGP.Networking`` and ``egp::networking`` facades and Superposition
nodes belong to the retired transport. Their declarations are not this API.
