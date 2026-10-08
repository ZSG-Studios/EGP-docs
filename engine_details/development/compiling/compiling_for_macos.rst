.. _doc_compiling_for_macos:

Compiling for macOS
===================

Requirements
------------

Install Xcode or its Command Line Tools, the macOS SDK, and xmake 3.1.1. Install MoltenVK through the Vulkan SDK when enabling Vulkan rendering.
For C# builds, install the .NET SDK selected by ``modules/mono/global.json``.
Use the platform package manager for system development libraries and verify
that xmake reports the pinned version with ``xmake --version``.

Building an editor
------------------

From the EGP repository root:

.. code-block:: shell

    xmake lua misc/scripts/build_egp.lua macos editor 8 .build/xmake-cache "dev_build=y"

The native graph generates resources, compiles and links the engine, captures
its actual API, and packages the matching C++ SDK in the final editor. Separate
variant caches retain the chosen architecture, compiler, precision, and flags.

Export templates
----------------

.. code-block:: shell

    xmake lua misc/scripts/build_egp.lua macos template_debug 8 .build/xmake-cache
    xmake lua misc/scripts/build_egp.lua macos template_release 8 .build/xmake-cache

Pass ``arch=arm64`` or ``arch=x86_64`` in the final options argument as
appropriate for the installed toolchain. Build each architecture explicitly;
packaging a universal binary requires matching component builds.

Optional dependencies
---------------------

The native dependency installer provides pinned packages:

.. code-block:: shell

    xmake lua misc/scripts/install_build_dependencies.lua accesskit

On macOS, use the same installer with ``angle`` if ANGLE is enabled. Install the
system SDK and Vulkan dependencies needed by your selected renderer before
building. See :ref:`doc_introduction_to_the_buildsystem` for options and
:ref:`doc_compiling_with_dotnet` for managed outputs.

Qualification
-------------

Use the final editor/template executables under ``bin/`` and their matching
symbols, assemblies, and extension SDK. Consult completed platform CI jobs and
:ref:`doc_egp_qualification` for tested configurations. A configured cross
compiler alone does not qualify rendering, physics, or gameplay on its target.
