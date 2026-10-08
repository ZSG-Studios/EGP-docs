.. _doc_visionos_intro:

Using visionOS
==============

EGP's visionOS configuration supports windowed Forward+ applications.
Set :ref:`Application > App Role
<class_EditorExportPlatformVisionOS_property_application/app_role>` to
**Window** in the export preset. A supported RenderingDevice driver is
required; the Mobile renderer is removed.

**Immersive** applications are unsupported. The retained visionOS XR API
does not establish immersive rendering support, and the export preset
reports the unsupported role. Do not use upstream instructions that switch
to Mobile rendering or initialize a visionOS immersive session.

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
describe a supported EGP immersive workflow.
