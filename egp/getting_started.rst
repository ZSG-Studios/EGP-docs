.. _doc_egp_getting_started:

Getting started with EGP
========================

Use an EGP editor and export templates built from the same engine revision.
Godot version strings alone do not identify EGP's native API or its bundled
C++ SDK. C# projects also require the matching GodotSharp assemblies and packages.

Building the editor
-------------------

Clone the `engine repository <https://github.com/ZSG-Studios/EGP>`__ and
initialize its pinned C++ SDK dependency:

.. code-block:: powershell

   git clone --recurse-submodules https://github.com/ZSG-Studios/EGP.git
   cd EGP
   .\misc\scripts\build_egp.ps1 -Setup
   .\misc\scripts\build_egp.ps1 -Local -Target editor

On Windows, install Visual Studio's C++ desktop workload, the Windows SDK
and the .NET SDK first. The launcher builds the native editor, embeds bindings
for its actual extension API, then generates and builds managed assemblies.
See :doc:`fastbuild` for export templates and distributed compilation.

For a native editor on another desktop platform, use Godot's inherited
:ref:`compilation instructions <doc_compiling_index>` and
``misc/scripts/build_egp_cpp_editor.py`` to embed the exact EGP API.
Check the :doc:`qualification` page before relying on a platform or feature.

Choosing a scripting API
------------------------

GDScript and C# use ordinary Godot scenes and nodes. Native extensions use
the editor's :doc:`built-in C++ extension tools <cpp_extensions>`.
Game code continues to use ``PhysicsServer2D/3D`` and ordinary physics nodes;
EGP selects Box2D and Box3D as the native backends.

Networking helpers are installed into an existing project from the engine root:

.. code-block:: powershell

   python misc/scripts/install_egp_net_helpers.py --project C:/Games/MyGame --languages gdscript csharp cpp

The destination must contain ``project.godot``. Installation always includes
the shared GDScript codec. C# and high-level C++ networking use that codec;
the low-level native session does not require it. Start with :doc:`networking`.

Exporting a game
----------------

Build matching ``template_debug`` and ``template_release`` targets, then
select those binaries in the project's export preset. Compile C++ extensions
for the matching Debug or Release configuration before exporting. C# games
require Mono templates and matching managed API packages. Test the relocated
export, including its PCK and native extension libraries.

See :doc:`migration` when importing an existing Godot project.
