.. _doc_visionos_intro:

Using visionOS
==============

EGP's visionOS configuration supports windowed Forward+ applications.
Set :ref:`Application > App Role
<class_EditorExportPlatformVisionOS_property_application/app_role>` to
**Window** in the export preset. A supported RenderingDevice driver is
required; the Mobile renderer is removed.

An opt-in **Immersive (experimental)** Forward+ path is available with Metal
and ``xr/visionos/experimental_forward_plus=true``. Foveation is disabled;
physical headset rendering, tracking, lifecycle and performance remain
unqualified. Follow :doc:`/egp/visionos_experimental` for the constrained startup,
export and Xcode device handoff profile. The Mobile renderer is not restored.

Headless tooling retains the dummy backend. Native platform compilation and
physical visionOS device behavior have separate qualification requirements;
see :ref:`doc_egp_qualification` for tested revisions and artifacts.

For the native export workflow, see :ref:`doc_exporting_for_visionos`.
For renderer and driver requirements, see :ref:`doc_renderers`.

.. _doc_visionos_sky_depth_write:

Retired immersive rendering guidance
------------------------------------

This bookmark is retained for older links. Upstream guidance for immersive
passthrough, depth reprojection, tracking and sky depth writes does not
describe the constrained experimental EGP Forward+ workflow.
