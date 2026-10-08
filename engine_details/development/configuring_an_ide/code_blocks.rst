.. _doc_configuring_an_ide_code_blocks:

Code::Blocks
============

These instructions configure the native engine source. For GDScript and C# game
editing, see :ref:`doc_external_editor` and :ref:`doc_c_sharp_setup_external_editor`.

Prepare a configuration
-----------------------

Install the platform compiler and SDK, then build a developer editor and export
its exact compilation database from the engine root:

.. code-block:: shell

    xmake lua misc/scripts/build_egp.lua linuxbsd editor 8 .build/xmake-cache "dev_build=y compiledb=y"

The ``compiledb=y`` option generates ``compile_commands.json`` through xmake's
native project exporter. Import that database where the IDE supports it, or
configure its C++ language service to use the generated compile commands. Select
the compiler matching the database's target and architecture. Regenerate the
database when changing native configuration options.

Build and debug
---------------

Create an external/custom build task with:

- Program: ``xmake`` or its absolute installed path.
- Working directory: the engine repository root.
- Arguments: ``lua misc/scripts/build_egp.lua linuxbsd editor 8 .build/xmake-cache "dev_build=y compiledb=y"``.

Choose the final executable published under ``bin/`` for the debugger and keep
its symbols from the same build. Set the working directory to the engine root
or pass ``--path <game-project>`` when debugging a game. The API bootstrap editor
is an internal build input and is not the application to debug.

Use a separate native variant cache for different architectures, sanitizers,
precision, or feature sets. See :ref:`doc_introduction_to_the_buildsystem` for
native options and :ref:`doc_compiling_with_dotnet` for managed builds.
