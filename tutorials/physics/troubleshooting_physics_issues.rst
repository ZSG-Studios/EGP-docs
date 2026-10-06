.. _doc_troubleshooting_physics_issues:

Troubleshooting EGP physics
===========================

Start by checking the generated class reference and :doc:`/egp/box2d` or
:doc:`/egp/box3d` for backend-specific support. EGP uses Box2D/Box3D; switching
to Godot Physics or Jolt is not a supported troubleshooting step.

Keep the configured tick rate and time scale fixed for deterministic profiles.
Match geometry, entity creation order, command sequences and gameplay inputs
when comparing trajectories. Scene RIDs are local handles and must not be
used as network entity identifiers.

For query failures, verify finite geometry, nonsingular transforms, shape
support and polygon vertex limits. Reproduce with a minimal scene using the
same binary and settings. Preserve the engine error output and fixture hashes.

Explicit world corrections do not restore SceneTree nodes. Trusted local
snapshots require compatible binaries and complete application-state restore;
see :doc:`/egp/explicit_world` and :doc:`/egp/prediction`.

Report reproducible EGP issues to the `EGP tracker
<https://github.com/ZSG-Studios/EGP/issues>`__. Include the source revision,
platform, editor/template identity and minimal reproduction project.
