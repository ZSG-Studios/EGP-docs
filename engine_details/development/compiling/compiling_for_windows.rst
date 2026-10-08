.. _doc_compiling_for_windows:

Compiling for Windows
=====================

Build EGP's Windows editor and export templates from the engine repository root.
For exporting an existing game, see :ref:`doc_exporting_for_windows`.

.. _doc_compiling_for_windows_install_vs:

Requirements
------------

Install Visual Studio's **Desktop development with C++** workload, the Windows
SDK, and xmake 3.1.1. Install the .NET SDK selected by ``modules/mono/global.json``
when building a C# engine. The pinned PowerShell launcher can install xmake:

.. code-block:: powershell

    .\misc\scripts\build_egp.ps1 -Setup

Select compiler components for each requested architecture. EGP supports native
MSVC and the platform's LLVM/MinGW toolchain routes; use the matching compiler,
SDK, runtime libraries, and feature configuration throughout a build.

Building
--------

The PowerShell launcher builds the native engine and matching managed outputs:

.. code-block:: powershell

    .\misc\scripts\build_egp.ps1 -Target editor -Jobs 8
    .\misc\scripts\build_egp.ps1 -Target template_debug -Jobs 8
    .\misc\scripts\build_egp.ps1 -Target template_release -Jobs 8

For a native-only editor, use the Lua launcher explicitly:

.. code-block:: shell

    xmake lua misc/scripts/build_egp.lua windows editor 8 .build/xmake-cache "dev_build=y module_mono_enabled=n"

Each option set receives its own cache. The final editor contains bindings
packaged from its actual API. Build templates and managed libraries from the
same revision; see :ref:`doc_compiling_with_dotnet` and
:ref:`doc_introduction_to_the_buildsystem`.

Architectures and toolchains
----------------------------

Pass ``arch=x86_64``, ``arch=x86_32``, or ``arch=arm64`` in the final options
argument. ``use_llvm=y`` requests LLVM. For example:

.. code-block:: shell

    xmake lua misc/scripts/build_egp.lua windows template_release 8 .build/xmake-cache "arch=arm64"

Compiler and runtime qualification is specific to the built artifact. Check
completed CI jobs for the chosen toolchain and feature set.

.. _doc_compiling_for_windows_installing_d3d12_requirements:

Optional graphics and accessibility SDKs
----------------------------------------

Install pinned optional dependencies using the native installer:

.. code-block:: shell

    xmake lua misc/scripts/install_build_dependencies.lua d3d12
    xmake lua misc/scripts/install_build_dependencies.lua accesskit

Enable the corresponding options only after installing their SDKs. The
PowerShell launcher's default profile uses ``d3d12=n accesskit=n``;
add overrides with ``-XmakeArgs`` when those features are required.
Rendered projects use Forward+ through an enabled RenderingDevice driver.
OpenGL and ANGLE are removed; headless tooling can use the dummy backend.

Outputs and debugging
---------------------

Final executables are published under ``bin/``. Debug symbols belong to the
same build as their executable. Launch the final editor or game with your IDE's
native debugger; do not distribute the internal API bootstrap executable.
Use :ref:`doc_introduction_to_the_buildsystem_debugging_symbols` for diagnostic
options and :ref:`doc_configuring_an_ide` for compilation-database indexing.
