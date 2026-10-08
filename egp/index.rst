.. _doc_egp:

EGP manual
==========

EGP is ZSG-Studios' fork of Godot Engine. It retains Godot's editor, scene
system and Forward+ rendering, and integrates Box2D, Box3D, Yojimbo,
native C++ extension tools and a Windows native xmake workflow.

Start with the EGP guides below before following inherited Godot tutorials.
Rendering, physics and multiplayer projects require particular attention during
migration. Rendered projects require a supported RenderingDevice driver;
headless servers and tooling retain the dummy backend. Web exports are unsupported.
The class reference is generated from EGP's engine sources.

.. toctree::
   :maxdepth: 2
   :caption: Getting started

   getting_started
   migration
   qualification

.. toctree::
   :maxdepth: 2
   :caption: Physics

   box2d
   box3d
   explicit_world

.. toctree::
   :maxdepth: 2
   :caption: Networking

   networking
   prediction
   networking_reference
   superposition
   physics_arena
   deterministic_demo
   helper_reference
   network_lab
   admission_testing
   language_testing

.. toctree::
   :maxdepth: 2
   :caption: Development

   cpp_extensions
   hot_reload
   xmake
   api_contract
   reference_workflow
   documentation
