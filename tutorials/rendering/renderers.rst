.. _doc_renderers:

Overview of rendering
=======================

EGP uses **Forward+** for rendered projects. It uses the **RenderingDevice**
backend with Vulkan, Direct3D 12 or Metal, depending on the platform and enabled
build features. Compatibility and Mobile renderers, OpenGL/OpenGL ES, ANGLE,
WebGL and WebXR are removed.

For implementation details, see :ref:`doc_internal_rendering_architecture`.
For tested revisions and platforms, see :ref:`doc_egp_qualification`.

Rendering methods, drivers and RenderingDevice
------------------------------------------------

The *rendering method* determines how the engine draws the scene. Forward+
uses clustered lighting and supports compute shaders, global illumination,
volumetric fog and screen-space effects. See :ref:`doc_list_of_features`.

The *rendering driver* communicates with the GPU through a graphics API.
Vulkan, Direct3D 12 and Metal have different platform, GPU and driver
requirements. A backend must be included in the engine build and supported
by the target device.

*RenderingDevice* is the abstraction between Forward+ and the graphics
driver. It also exposes GPU resources and compute operations to scripts and
extensions. Changing the driver does not select another rendering method.

Creating or migrating a project
---------------------------------

New rendered projects use Forward+. For an existing project, set
:ref:`Rendering > Renderer > Rendering Method
<class_ProjectSettings_property_rendering/renderer/rendering_method>` to
``forward_plus``. Update its mobile override to ``forward_plus`` as well.
Mobile platforms are distinct from the removed Mobile renderer.

Selections such as ``mobile`` and ``gl_compatibility`` are rejected. There is
no fallback renderer for devices without a supported RenderingDevice driver.
Test the project's materials, lighting and frame budget on its target
hardware after migrating.

Driver selection and fallback
-------------------------------

The available drivers depend on the platform and build. RenderingDevice
driver fallback may be configured where the platform supports it, such as
between Vulkan and Direct3D 12 on Windows. It does not restore OpenGL,
Compatibility or Mobile rendering.

Use :ref:`RenderingServer.get_current_rendering_method()
<class_RenderingServer_method_get_current_rendering_method>` and
:ref:`RenderingServer.get_current_rendering_driver_name()
<class_RenderingServer_method_get_current_rendering_driver_name>` to inspect
the active method and driver. Project settings describe the requested
configuration; they do not prove that a GPU can initialize it.

Headless servers and tooling
------------------------------

The dummy rendering backend remains available for headless dedicated
servers and tooling. Start the engine with ``--headless`` when a GPU and
display are unnecessary. See :ref:`doc_exporting_for_dedicated_servers`.

Web support
-------------

Browser rendering, Web exports and WebXR are unsupported at this revision.
Removing WebGL does not provide a RenderingDevice web backend. Use a
supported native target for rendered projects.
