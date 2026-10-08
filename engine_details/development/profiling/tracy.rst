.. _doc_profiler_tracy:

Tracy
=====

.. seealso:: Please see the :ref:`tracing profiler instructions <doc_tracing_profilers>` for more information.

`Tracy <https://github.com/wolfpld/tracy>`__ is an Open Source profiler that runs on a wide variety of platforms,
including Windows, Linux, and macOS. While it is primarily a tracing profiler,
it can also periodically sample data like a
:ref:`sampling profiler <doc_sampling_profilers>`, giving some of the benefits
of both approaches.

Build Godot with Tracy support
------------------------------

First, clone the latest version of the Tracy source code ("0.13.0" at the
time of writing) using Git:

.. code-block:: shell

    git clone -b v0.13.0 --single-branch https://github.com/wolfpld/tracy.git

This will create a ``tracy`` directory - you can place this anywhere.

Next, build the release templates for your platform using ``xmake lua misc/scripts/build_egp.lua <platform> editor 8 .build/xmake-cache``, but adding
the ``profiler=tracy profiler_path=path/to/tracy`` arguments with the real path
to the ``tracy`` directory, as well as ``debug_symbols=yes`` to allow Tracy's
sampling features to work.

.. note::

    You don't have to build release templates, you could also build debug
    templates, or even the editor. However, it's generally recommended to
    profile release templates, because that is the version your players will
    use, and it will perform differently than other types of builds.

For example, to build release templates for Windows:

.. code-block:: shell

    xmake lua misc/scripts/build_egp.lua windows template_release 8 .build/xmake-cache "debug_symbols=yes profiler=tracy profiler_path=path/to/tracy"

Get the Tracy "server"
----------------------

In Tracy terminology, the application you are profiling is the "client", and
the one receiving the data is the "server".

If you are on Windows, you can download a pre-built ``tracy-profiler.exe``
from the Tracy `releases page <https://github.com/wolfpld/tracy/releases>`_.

However, if you're on Linux or macOS, you'll either need to find a pre-built
binary from a package manager (like ``brew`` or ``nix``), or build it from
source yourself.

.. note::

    If you do use a pre-built binary, be sure to use the same version that
    you used when building Godot.

Install the matching Tracy profiler
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use a Tracy profiler distribution compatible with the client version bundled
in EGP. Keep the profiler and engine client versions matched, then launch the
profiler executable to receive or inspect captures. The profiler is an external
tool; it does not replace EGP's native xmake engine build.

Record a trace
--------------

Launch the Tracy server - you'll see something like this:

.. image:: img/cpp_profiler_tracy_start.webp

Press "connect". This will ensure tracy makes a connection immediately when
the game launches. If you forget to press "connect", Tracy will store system
events in RAM, which can quickly blow up your memory usage (see the
``TRACY_ON_DEMAND`` documentation).

Now, export your game using the release templates you built above, and run it.
As soon as both are running, and you have pressed the "Connect" button in
Tracy, you'll see data coming in:

.. image:: img/cpp_profiler_tracy_recording.webp

When you think you've gathered enough data, press the "Stop" button. If you
clicked somewhere and the box with the "Stop" button disappeared, you can
click the top-left most icon to bring it back.

Examining the trace
-------------------

Here are some of the basic controls:

- Zoom in/out with the mouse wheel
- Right click and drag to move forward/backward on the timeline
- In the top bar, click the left and right arrow buttons by "Frames" to move a single frame on the timeline

To learn more, see the
`Tracy manual <https://github.com/wolfpld/tracy/releases/latest/download/tracy.pdf>`_.
