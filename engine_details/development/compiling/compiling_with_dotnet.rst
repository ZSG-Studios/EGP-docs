.. _doc_compiling_with_dotnet:

Compiling with .NET
===================

.. highlight:: shell

Requirements
------------

- The `.NET SDK <https://dotnet.microsoft.com/download>`_ selected by
  ``modules/mono/global.json``.

  You can use ``dotnet --info`` to check which .NET SDK versions are installed.

Enable the .NET module
----------------------

.. note:: C# support for Godot has historically used the
          `Mono <https://www.mono-project.com/>`_ runtime instead of the
          `.NET Runtime <https://github.com/dotnet/runtime>`_ and internally
          many things are still named ``mono`` instead of ``dotnet`` or
          otherwise referred to as ``mono``.

By default, the .NET module is disabled when building. To enable it, add the
option ``module_mono_enabled=yes`` to the xmake command line, while otherwise
following the instructions for building the desired Godot binaries.

Generate the glue
-----------------

Parts of the sources of the managed libraries are generated from the ClassDB.
These source files must be generated before building the managed libraries.
Generate them with the matching .NET-enabled EGP editor binary, running it with
the parameters ``--headless --generate-mono-glue`` followed by the path to an
output directory.
This path must be ``modules/mono/glue`` in the Godot directory:

::

    <godot_binary> --headless --generate-mono-glue modules/mono/glue

This command will tell Godot to generate the C# bindings for the Godot API at
``modules/mono/glue/GodotSharp/GodotSharp/Generated``, and the C# bindings for
the editor tools at ``modules/mono/glue/GodotSharp/GodotSharpEditor/Generated``.
Once these files are generated, you can build Godot's managed libraries for all
the desired targets without having to repeat this process.

``<godot_binary>`` refers to the editor binary you compiled with the .NET module
enabled. Its exact name will differ based on your system and configuration, but
should be of the form ``bin/godot.<platform>.editor.<arch>.mono``, e.g.
``bin/godot.linuxbsd.editor.x86_64.mono`` or
``bin/godot.windows.editor.x86_32.mono.exe``. Be especially aware of the
**.mono** suffix! If you've previously compiled Godot without .NET support, you
might have similarly named binaries without this suffix. These binaries can't be
used to generate the .NET glue.

.. note:: The glue sources must be regenerated every time the ClassDB-registered
          API changes. That is, for example, when a new method is registered to
          the scripting API or one of the parameters of such a method changes.
          Godot will print an error at startup if there is an API mismatch
          between ClassDB and the glue sources.

Building the managed libraries
------------------------------

Generate the C# glue with the matching final Mono editor, then build API
assemblies, editor tools, and SDK packages with the native Lua launcher:

.. code-block:: shell

    <godot_binary> --headless --generate-mono-glue modules/mono/glue
    xmake lua build/xmake/managed.lua <godot_binary> <platform> single

Use ``double`` instead of ``single`` only when the executable was built with
that precision. Supported managed platform names are ``windows``, ``linuxbsd``,
``macos``, ``android``, and ``ios``. Install the .NET SDK selected by
``modules/mono/global.json``. Results are published under ``bin/GodotSharp``.
The Windows ``build_egp.ps1`` launcher performs these steps automatically.

Unlike "classical" Godot builds, when building with the .NET module enabled
(and depending on the target platform), a data directory may be created both
for the editor and for exported projects. This directory is important for
proper functioning and must be distributed together with Godot.
More details about this directory in
:ref:`Data directory<compiling_with_dotnet_data_directory>`.

Managed build options
~~~~~~~~~~~~~~~~~~~~~

Pass the target platform explicitly to the native managed launcher. The editor
used for glue generation must match the native API and precision of the assembly
build. For example, after building a Windows Mono editor:

.. code-block:: shell

    <editor> --headless --generate-mono-glue modules/mono/glue
    xmake lua build/xmake/managed.lua <editor> windows single

Use ``double`` for a native engine compiled with ``precision=double``. Add
``no-deprecated`` when the engine was compiled with ``deprecated=no``. For local
NuGet development, register a package source and pass its path to the launcher:

.. code-block:: shell

    dotnet nuget add source <local-source> --name EGPDevelopment
    xmake lua build/xmake/managed.lua <editor> windows single "push-nupkgs-local=<local-source>"

Distribute the matching ``GodotSharp`` directory with the editor. Build native
export templates separately with ``module_mono_enabled=yes``; project assemblies
and exported managed data are produced by the editor's export workflow.

.. _compiling_with_dotnet_data_directory:

Data directory
--------------

The data directory is a dependency for Godot binaries built with the .NET module
enabled. It contains important files for the correct functioning of Godot. It
must be distributed together with the Godot executable.

Editor
~~~~~~

The name of the data directory for the Godot editor will always be
``GodotSharp``. This directory contains an ``Api`` subdirectory with the Godot
API assemblies and a ``Tools`` subdirectory with the tools required by the
editor, like the ``GodotTools`` assemblies and its dependencies.

On macOS, if the Godot editor is distributed as a bundle, the ``GodotSharp``
directory may be placed in the ``<bundle_name>.app/Contents/Resources/``
directory inside the bundle.

Export templates
~~~~~~~~~~~~~~~~

The data directory for exported projects is generated by the editor during the
export. It is named ``data_<APPNAME>_<ARCH>``, where ``<APPNAME>`` is the
application name as specified in the project setting ``application/config/name``
and ``<ARCH>`` is the current architecture of the export.

In the case of multi-architecture exports multiple such data directories will be
generated.

Command-line options
--------------------

The following is the list of command-line options available when building with
the .NET module:

- **module_mono_enabled**\ =yes | **no**

  - Build Godot with the .NET module enabled.
