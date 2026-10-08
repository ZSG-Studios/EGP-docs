.. _doc_introduction_to_the_buildsystem:

Introduction to the build system
================================

EGP uses native xmake targets for source generation, compilation, archives,
linking, and dependency tracking. Lua generators and native host tools produce
engine resources and the C++ SDK. Install xmake 3.1.1 and the compiler/SDK for
your target platform, then run commands from the engine repository root.

Building an editor
------------------

The launcher configures a separate cache for each platform, architecture,
target, and set of options. For a Linux developer editor:

.. code-block:: shell

    xmake lua misc/scripts/build_egp.lua linuxbsd editor 8 .build/xmake-cache "dev_build=y"

Replace ``linuxbsd`` with ``windows`` or ``macos`` for another desktop host.
The fourth argument selects parallel compile jobs. Keep editor, templates,
managed assemblies, and extension SDKs from the same source revision.

The editor target first builds an API-export bootstrap executable, captures
its actual ClassDB API, generates matching extension bindings, and links the
final SDK-bearing editor. The bootstrap executable is an internal build input.

.. _doc_introduction_to_the_buildsystem_resulting_binary:

Resulting binaries
------------------

Executables are published under ``bin/``. Their names include platform, target,
architecture, and enabled variants such as ``.dev``, ``.double``, and ``.mono``.
Use the final executable identified by the build output. Generated resources,
objects, libraries, and configuration caches belong under the variant build
folder and should not be added to source control.

.. _doc_introduction_to_the_buildsystem_target:

Editor and export templates
---------------------------

Supported target names are ``editor``, ``template_debug``, and
``template_release``. Build each required target with the same feature options:

.. code-block:: shell

    xmake lua misc/scripts/build_egp.lua windows template_debug 8 .build/xmake-cache
    xmake lua misc/scripts/build_egp.lua windows template_release 8 .build/xmake-cache

Export templates contain the runtime. The editor also includes development UI
and its embedded, pre-generated C++ SDK.

.. _doc_introduction_to_the_buildsystem_development_and_production_aliases:
.. _doc_introduction_to_the_buildsystem_debugging_symbols:

Development and diagnostics
---------------------------

Pass options as the launcher's final quoted argument. For example:

.. code-block:: shell

    xmake lua misc/scripts/build_egp.lua linuxbsd editor 8 .build/xmake-cache "dev_build=y debug_symbols=y tests=y"

Options such as ``use_asan=y``, ``use_ubsan=y``, or ``use_tsan=y`` select a
sanitizer where the chosen compiler supports it. Sanitizer builds need separate
caches and runtime tests. ``use_llvm=y`` selects the platform's LLVM toolchain.

The native configuration menu lists available options:

.. code-block:: shell

    xmake f --help

.. _doc_overriding_build_options:

Configurations and architectures
--------------------------------

The launcher accepts ``KEY=VALUE`` options and normalizes boolean values.
For a Windows ARM64 template:

.. code-block:: shell

    xmake lua misc/scripts/build_egp.lua windows template_release 8 .build/xmake-cache "arch=arm64"

Platform SDKs and toolchains must be installed for the requested architecture.
The graph retains platform feature gates; an available target name alone does
not establish runtime qualification for a particular feature or platform.

Use ``compiledb=y`` to export the compilation database for IDE indexing:

.. code-block:: shell

    xmake lua misc/scripts/build_egp.lua linuxbsd editor 8 .build/xmake-cache "dev_build=y compiledb=y"

xmake retains the selected configuration. ``xmake clean editor`` cleans that
configuration's editor outputs; changing launcher options selects a separate
variant rather than overwriting another configuration's objects.

.. _doc_buildsystem_custom_modules:

Custom modules
--------------

Native modules have source and registration files under ``modules/<name>``.
Their Lua configuration and source-selection recipes live under
``build/xmake/recipes/modules/<name>``. Register the module's feature option
in ``build/xmake/options.lua`` and follow :ref:`doc_custom_modules_in_cpp`.
Each recipe keeps its include paths, defines, and compiler flags local to its
module. Review native source and generator dependencies when adding a module.

Managed builds
--------------

Set ``module_mono_enabled=y`` for a C# engine and generate/build the managed
assemblies from that exact executable. The Windows PowerShell launcher performs
this step automatically; direct Lua builds use the separate native managed
launcher described in :ref:`doc_compiling_with_dotnet`.

See the :doc:`EGP build guide </egp/xmake>` for installation, isolated caches,
SDK packaging, and platform qualification.
