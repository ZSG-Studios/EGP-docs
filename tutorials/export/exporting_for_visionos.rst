.. _doc_exporting_for_visionos:

Exporting for visionOS
======================

.. seealso::

    This page describes how to export an EGP project to visionOS.
    If you're looking to compile export template binaries from source instead,
    see :ref:`doc_compiling_for_visionos`.

Exporting instructions for visionOS are very similar to :ref:`doc_exporting_for_ios`.
You can refer to it for more details about the Xcode workflow.

Requirements
------------

-  `Xcode <https://developer.apple.com/xcode/>`_ (from the macOS App Store).
-  An Apple account, for code-signing (`free for on-device testing <https://developer.apple.com/support/compare-memberships/>`_).

.. attention::

    Projects written in C# are currently not supported on visionOS, as
    the :ref:`.NET runtime <doc_c_sharp_platforms>` does not support visionOS.

App Role
--------

Use the **Window** role to present the project in a flat window with
Forward+ and Metal. A supported RenderingDevice driver is required.
The **Immersive (experimental)** role requires Metal and
``xr/visionos/experimental_forward_plus=true``. The initial path disables
foveation, MSAA and temporal AA/upscaling, requires HDR 2D and 3D scale 1.0,
and uses the supplied Xcode launch profile's native Metal hazard tracking.
Physical headset rendering, tracking, lifecycle and performance are unqualified.
See :doc:`/egp/visionos_experimental` for the exact fixture, export and device
handoff instructions. Upstream Mobile-renderer instructions do not apply.

Native compilation, export configuration and physical visionOS device
behavior have separate qualification requirements. See
:ref:`doc_egp_qualification` for tested revisions and artifacts.
