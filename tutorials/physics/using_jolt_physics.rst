.. _doc_using_jolt_physics:

3D physics in EGP
=================

EGP uses Box3D as its sole native 3D physics backend. The Jolt and Godot
Physics 3D implementations and their solver-specific settings are removed.
Ordinary physics nodes and ``PhysicsServer3D`` remain the scene-facing APIs.

Read :doc:`/egp/box3d` for integration details and outstanding compatibility
gates. Use :doc:`/egp/explicit_world` for fixed-tick application worlds,
ordered commands and trusted local snapshots. Check the generated class
reference for the available joint, shape and query APIs.
