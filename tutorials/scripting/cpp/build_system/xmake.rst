.. _doc_godot_cpp_build_system:

Building C++ extensions with xmake
==================================

EGP's editor creates a native ``xmake.lua`` extension project and extracts the
matching, pre-generated SDK. Keep this SDK with its engine revision: its
``sdk.json`` binds the actual API, precision, pointer size, and source files.
See :doc:`the editor workflow </egp/cpp_extensions>` for scaffolding and diagnostics.

From the extension project directory:

.. code-block:: shell

    xmake f -P /absolute/extension --egp_cpp_sdk=/absolute/sdk -p windows -a x64 -m debug
    xmake -P /absolute/extension -b extension

The ``godot-cpp`` target builds or restores the matched native library; the
``extension`` target builds the game's shared library. ``-m release`` selects
the release variant. Run configuration from the project directory to keep
xmake's configuration and lock files local to that project.

The generated descriptor names the platform, architecture, and library for each
mode. Preserve its entry symbol and reload contract when editing the project.
Build and test exported games with their matching templates before distributing
libraries. Host compilation alone does not establish cross-platform support.
