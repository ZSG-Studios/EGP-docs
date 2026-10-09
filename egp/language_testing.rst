.. _doc_egp_language_testing:


Generated language bindings
===========================

GDScript, generated ``Godot.SuperposSession`` C# and generated
``godot::SuperposSession`` C++ bindings call the same native ClassDB API.
Generate both language SDKs from the intended editor and keep public C++
headers compatible with C++17. The core uses C++23 privately.

Old helper facades, RPC/spawner nodes and their receipts are retired.
See :doc:`helper_reference`, :doc:`networking_reference` and :doc:`qualification`.
