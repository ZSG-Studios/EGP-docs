:allow_comments: False

.. _doc_configuring_an_ide:

Configuring an IDE
==================

We assume that you have already `cloned <https://github.com/godotengine/godot>`_
and :ref:`compiled <toc-devel-compiling>` Godot.

You can easily develop Godot with any text editor and by invoking ``xmake lua misc/scripts/build_egp.lua <platform> editor 8 .build/xmake-cache``
on the command line, but if you want to work with an IDE (Integrated
Development Environment), here are setup instructions for some popular ones:

.. toctree::
   :maxdepth: 1
   :name: toc-devel-configuring_an_ide

   android_studio
   clion
   code_blocks
   kdevelop
   qt_creator
   rider
   visual_studio
   visual_studio_code
   xcode

It is possible to use other IDEs, but their setup is not documented yet.

If your editor supports the `language server protocol <https://microsoft.github.io/language-server-protocol/>`__,
you can use `clangd <https://clangd.llvm.org>`__ for completion, diagnostics, and more.
You can generate a compilation database for use with clangd one of two ways:

.. code-block:: shell

   # Generate compile_commands.json while compiling
   xmake lua misc/scripts/build_egp.lua <platform> editor 8 .build/xmake-cache "compiledb=yes"

   # Generate compile_commands.json without compiling
   xmake lua misc/scripts/build_egp.lua <platform> editor 8 .build/xmake-cache "compiledb=yes"
