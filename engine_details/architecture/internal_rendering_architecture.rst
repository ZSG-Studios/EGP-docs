.. _doc_internal_rendering_architecture:

Internal rendering architecture
===============================

This page describes EGP's Forward+ rendering architecture inherited from
Godot 4. Compatibility and Mobile renderers and OpenGL backends are removed.
See :ref:`doc_renderers` for current driver and platform requirements.

The goal of this page is to document design decisions taken to best suit
`Godot's design philosophy <https://contributing.godotengine.org/en/latest/development/engine/best_practices.html>`__,
while providing a starting point for new rendering contributors.

If you have questions about rendering internals not answered here, feel free to
ask in the ``#rendering`` channel of the
`Godot Contributors Chat <https://chat.godotengine.org/channel/rendering>`__.

.. note::

    If you have difficulty understanding concepts on this page, it is
    recommended to go through an OpenGL tutorial such as
    `LearnOpenGL <https://learnopengl.com/>`__.

    Modern low-level APIs (Vulkan/Direct3D 12/Metal) require intermediate
    knowledge of higher-level APIs (OpenGL/Direct3D 11) to be used
    effectively. Thankfully, contributors rarely need to work directly with
    low-level APIs. EGP's Forward+ renderer uses RenderingDevice, our abstraction
    over Vulkan/Direct3D 12/Metal. The linked OpenGL tutorial teaches general
    graphics concepts; OpenGL is not an EGP backend.

.. _doc_internal_rendering_architecture_methods:

Rendering methods
-----------------

Forward+
~~~~~~~~

This is a forward renderer that uses a *clustered* approach to lighting.

Clustered lighting uses a compute shader to group lights into a 3D frustum
aligned grid. Then, at render time, pixels can lookup what lights affect the
grid cell they are in and only run light calculations for lights that might
affect that pixel.

The cost depends on light coverage, shader work and GPU architecture. Profile
the scene on its target hardware, including tile-based mobile GPUs.

.. _doc_internal_rendering_architecture_compatibility:

Retired rendering methods
~~~~~~~~~~~~~~~~~~~~~~~~~

EGP removes the upstream Mobile and Compatibility implementations. Their
tile-based and legacy OpenGL pipelines are not alternative rendering paths
in this fork. Headless servers and tooling retain the dummy backend.

Why not deferred rendering?
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Forward rendering generally provides a better tradeoff for performance versus
flexibility, especially when a clustered approach to lighting is used. While
deferred rendering can be faster in some cases, it's also less flexible and
requires using hacks to be able to use MSAA. Since games with a less realistic
art style can benefit a lot from MSAA, we chose to go with forward rendering for
Godot 4 (like Godot 3).

That said, parts of the forward renderer *are* performed with a deferred approach
to allow for some optimizations when possible. This applies to VoxelGI and SDFGI
in particular.

A clustered deferred renderer may be developed in the future. This renderer
could be used in situations where performance is favored over flexibility.

Rendering drivers
-----------------

EGP's RenderingDevice backend supports the following graphics APIs, depending
on the platform and enabled build features:

Vulkan
~~~~~~

This is the main driver in Godot 4, with most of the development focus going
towards this driver.

Vulkan 1.0 is required as a baseline, with optional Vulkan 1.1 and 1.2 features
used when available. `volk <https://github.com/zeux/volk>`__ is used as a Vulkan
loader, and
`Vulkan Memory Allocator <https://github.com/GPUOpen-LibrariesAndSDKs/VulkanMemoryAllocator>`__
is used for memory management.

The Forward+
:ref:`doc_internal_rendering_architecture_methods` are supported when using the
Vulkan driver.

**Vulkan context creation:**

- `drivers/vulkan/rendering_context_driver_vulkan.cpp <https://github.com/godotengine/godot/blob/4.6/drivers/vulkan/rendering_context_driver_vulkan.cpp>`__

**Direct3D 12 context creation:**

- `drivers/d3d12/rendering_context_driver_d3d12.cpp <https://github.com/godotengine/godot/blob/4.6/drivers/d3d12/rendering_context_driver_d3d12.cpp>`__

Direct3D 12
~~~~~~~~~~~

Like Vulkan, the Direct3D 12 driver targets modern platforms only. It is
designed to target both Windows and Xbox (whereas Vulkan can't be used directly on Xbox).

The Forward+ :ref:`doc_internal_rendering_architecture_methods` can be
used with Direct3D 12.

:ref:`doc_internal_rendering_architecture_core_shaders` are shared with the
Vulkan renderer. Shaders are transpiled from
:abbr:`SPIR-V (Standard Portable Intermediate Representation)` to
:abbr:`DXIL (DirectX Intermediate Language)` using
Mesa NIR (`more information <https://godotengine.org/article/d3d12-adventures-in-shaderland/>`__).

**This driver is still experimental and only available in Godot 4.3 and later.**
While Direct3D 12 allows supporting Direct3D-exclusive features on Windows 11 such
as windowed optimizations and Auto HDR, Vulkan is still recommended for most projects.
See the `pull request that introduced Direct3D 12 support <https://github.com/godotengine/godot/pull/70315>`__
for more information.

Metal
~~~~~

Godot provides a native Metal driver that works on all Apple Silicon hardware
(macOS ARM). Compared to using the MoltenVK translation layer, this is
significantly faster, particularly in CPU-bound scenarios.

The Forward+ :ref:`doc_internal_rendering_architecture_methods` can be
used with Metal.

:ref:`doc_internal_rendering_architecture_core_shaders` are shared with the
Vulkan renderer. Shaders are transpiled from GLSL to :abbr:`MSL (Metal Shading Language)`
using SPIRV-Cross.

Godot also supports Metal rendering via `MoltenVK <https://github.com/KhronosGroup/MoltenVK>`__,
which is used as a fallback when native Metal support is not available (e.g. on x86 macOS).

Since Godot 4.7, Metal 4 is now used when supported. All Apple Silicon hardware
supports Metal 4, but it must be running macOS 26 or later, or iOS 26 or later.
Metal 3 is automatically used as a fallback on older macOS and iOS versions.
See the `pull request that introduced Metal 4 support <https://github.com/godotengine/godot/pull/114484>`__
for more information.

Summary of rendering drivers/methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following rendering API + rendering method combinations are currently possible:

- Vulkan + Forward+ (optionally through MoltenVK on macOS and iOS)
- Direct3D 12 + Forward+
- Metal + Forward+

Each combination has its own limitations and performance characteristics. Make
sure to test changes with the target platforms and enabled RenderingDevice
drivers before publishing them.

RenderingDevice abstraction
---------------------------

To make the complexity of modern low-level graphics APIs more manageable,
Godot uses its own abstraction called RenderingDevice.

This means that when writing code for modern rendering methods, you don't
actually use the Vulkan, Direct3D 12, or Metal APIs directly. While this is still
lower-level than an API like OpenGL, this makes working on the renderer easier,
as RenderingDevice will abstract many API-specific quirks for you. The
RenderingDevice presents a similar level of abstraction as WebGPU.

**Vulkan RenderingDevice implementation:**

- `drivers/vulkan/rendering_device_driver_vulkan.cpp <https://github.com/godotengine/godot/blob/4.6/drivers/vulkan/rendering_device_driver_vulkan.cpp>`__

**Direct3D 12 RenderingDevice implementation:**

- `drivers/d3d12/rendering_device_driver_d3d12.cpp <https://github.com/godotengine/godot/blob/4.6/drivers/d3d12/rendering_device_driver_d3d12.cpp>`__

**Metal RenderingDevice implementation:**

- `drivers/metal/rendering_device_driver_metal.cpp <https://github.com/godotengine/godot/blob/master/drivers/metal/rendering_device_driver_metal.cpp>`__ - Metal 4
- `drivers/metal/rendering_device_driver_metal3.cpp <https://github.com/godotengine/godot/blob/master/drivers/metal/rendering_device_driver_metal3.cpp>`__ - Metal 3

Core rendering classes architecture
-----------------------------------

This diagram represents the structure of rendering classes in Godot, including the RenderingDevice abstraction:

.. image:: img/rendering_architecture_diagram.webp

`View at full size <https://raw.githubusercontent.com/godotengine/godot-docs/master/engine_details/architecture/img/rendering_architecture_diagram.webp>`__

.. _doc_internal_rendering_architecture_core_shaders:

Core shaders
------------

While shaders in Godot projects are written using a
:ref:`custom language inspired by GLSL <doc_shading_language>`, core shaders are
written directly in GLSL.

These core shaders are embedded in the editor and export template binaries at
compile-time. To see any changes you've made to those GLSL shaders, you need to
recompile the editor or export template binary.

Some material features such as height mapping, refraction and proximity fade are
not part of core shaders, and are performed in the default BaseMaterial3D using
the Godot shader language instead (not GLSL). This is done by procedurally
generating the required shader code depending on the features enabled in the
material.

By convention, shader files with ``_inc`` in their name are included in other
GLSL files for better code reuse. Standard GLSL preprocessing is used to achieve
this.

.. warning::

    Core material shaders will be used by every material in the scene – both
    with the default BaseMaterial3D and custom shaders. As a result, these
    shaders must be kept as simple as possible to avoid performance issues and
    ensure shader compilation doesn't become too slow.

    If you use ``if`` branching in a shader, performance may decrease as
    :abbr:`VGPR (Vector General-Purpose Register)` usage will increase in the
    shader. This happens even if all pixels evaluate to ``true`` or ``false`` in
    a given frame.

    If you use ``#if`` preprocessor branching, the number of required shader
    versions will increase in the scene. In a worst-case scenario, adding a
    single boolean ``#define`` can *double* the number of shader versions that
    may need to be compiled in a given scene. In some cases, Vulkan
    specialization constants can be used as a faster (but more limited)
    alternative.

    This means there is a high barrier to adding new built-in material features
    in Godot, both in the core shaders and BaseMaterial3D. While BaseMaterial3D
    can make use of dynamic code generation to only include the shader code if
    the feature is enabled, it'll still require generating more shader versions
    when these features are used in a project. This can make shader compilation
    stutter more noticeable in complex 3D scenes.

    See
    `The Shader Permutation Problem <https://therealmjp.github.io/posts/shader-permutations-part1/>`__
    and
    `Branching on a GPU <https://medium.com/@jasonbooth_86226/branching-on-a-gpu-18bfc83694f2>`__
    blog posts for more information.

**Core GLSL material shaders:**

- Forward+: `servers/rendering/renderer_rd/shaders/forward_clustered/scene_forward_clustered.glsl <https://github.com/godotengine/godot/blob/4.6/servers/rendering/renderer_rd/shaders/forward_clustered/scene_forward_clustered.glsl>`__

**Material shader generation:**

- `scene/resources/material.cpp <https://github.com/godotengine/godot/blob/4.6/scene/resources/material.cpp>`__

**Other GLSL shaders for Forward+ rendering:**

- `servers/rendering/renderer_rd/shaders/ <https://github.com/godotengine/godot/blob/4.6/servers/rendering/renderer_rd/shaders/>`__
- `modules/lightmapper_rd/ <https://github.com/godotengine/godot/blob/4.6/modules/lightmapper_rd>`__


2D and 3D rendering separation
------------------------------

.. note::

    Forward+ separates 2D and 3D rendering buffers. Multiple Viewports can be
    used when independent 2D resolution scaling is needed.

2D and 3D are rendered to separate buffers, as 2D rendering in Godot is performed
in :abbr:`LDR (Low Dynamic Range)` sRGB-space while 3D rendering uses
:abbr:`HDR (High Dynamic Range)` linear space.

The color format used for 2D rendering is RGB8 (RGBA8 if the **Transparent**
property on the Viewport is enabled). 3D rendering uses a 24-bit unsigned
normalized integer depth buffer, or 32-bit signed floating-point if a 24-bit
depth buffer is not supported by the hardware. 2D rendering does not use a depth
buffer.

3D resolution scaling is performed differently depending on whether bilinear or
FSR 1.0 scaling is used. When bilinear scaling is used, no special upscaling
shader is run. Instead, the viewport's texture is stretched and displayed with a
linear sampler (which makes the filtering happen directly on the hardware). This
allows maximizing the performance of bilinear 3D scaling.

The ``configure()`` function in RenderSceneBuffersRD reallocates the 2D/3D
buffers when the resolution or scaling changes.

.. UPDATE: Planned feature. When dynamic resolution scaling is supported,
.. update this paragraph.

Dynamic resolution scaling isn't supported yet, but is planned in a future Godot
release.

**2D and 3D rendering buffer configuration C++ code:**

- `servers/rendering/renderer_rd/storage_rd/render_scene_buffers_rd.cpp <https://github.com/godotengine/godot/blob/4.6/servers/rendering/renderer_rd/storage_rd/render_scene_buffers_rd.cpp>`__

**FSR 1.0:**

- `servers/rendering/renderer_rd/effects/fsr.cpp <https://github.com/godotengine/godot/blob/4.6/servers/rendering/renderer_rd/effects/fsr.cpp>`__
- `thirdparty/amd-fsr/ <https://github.com/godotengine/godot/tree/master/thirdparty/amd-fsr>`__

2D rendering techniques
-----------------------

2D light rendering is performed in a single pass to allow for better performance
with large amounts of lights.

All rendering methods feature 2D batching to improve performance, which is
especially noticeable with lots of text on screen.

MSAA can be enabled in 2D to provide "automatic" line and polygon antialiasing,
but FXAA does not affect 2D rendering as it's calculated before 2D rendering
begins. Godot's 2D drawing methods such as the Line2D node or some CanvasItem
``draw_*()`` methods provide their own way of antialiasing based on triangle
strips and vertex colors, which don't require MSAA to work.

A 2D signed distance field representing LightOccluder2D nodes in the viewport is
automatically generated if a user shader requests it. This can be used for
various effects in custom shaders, such as 2D global illumination. It is also
used to calculate particle collisions in 2D.

**2D SDF generation GLSL shader:**

- `servers/rendering/renderer_rd/shaders/canvas_sdf.glsl <https://github.com/godotengine/godot/blob/4.6/servers/rendering/renderer_rd/shaders/canvas_sdf.glsl>`__

3D rendering techniques
-----------------------

Reverse Z
~~~~~~~~~

All of Godot's renderers use reverse Z. This means that the depth buffer is
inverted, with ``1.0`` representing the near plane and ``0.0`` representing
the far plane. This allows for
`better precision <https://developer.nvidia.com/content/depth-precision-visualized>`__,
especially at long distances.

Batching and instancing
~~~~~~~~~~~~~~~~~~~~~~~

In the Forward+ renderer, Vulkan instancing is used to group rendering of
identical opaque or alpha-tested objects for performance. (Alpha-blended objects
are never instanced.) This is not as fast as static mesh merging, but it still
allows instances to be culled individually.

Light, decal and reflection probe rendering
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Forward+ renderer uses clustered lighting. Clusters limit lighting work to
lights that may affect the visible pixels, subject to the configured cluster
budget. Cost depends on screen coverage, shader work and shadow rendering.

Forward+ also supports rendering up to 8 directional lights at the
same time (albeit with lower shadow quality when more than one light has shadows
enabled).

.. UPDATE: Planned feature. When static and dynamic shadow rendering are
.. separated, update this paragraph.

Lights without shadows are much cheaper than lights with
shadows. To improve performance, lights are only updated when the light is
modified or when objects in its radius are modified. Godot currently doesn't
separate static shadow rendering from dynamic shadow rendering, but this is
planned in a future release.

Clustering is also used for reflection probes and decal rendering in the
Forward+ renderer.

Area lights make use of the
`Linearly Transformed Cosines <https://eheitzresearch.wordpress.com/757-2/>`__
technique.

Shadow mapping
~~~~~~~~~~~~~~

Forward+ uses
:abbr:`PCF (Percentage Closer Filtering)` to filter shadow maps and create a
soft penumbra. Instead of using a fixed PCF pattern, these methods use a vogel
disk pattern which allows for changing the number of samples and smoothly
changing the quality.

Godot also supports percentage-closer soft shadows (PCSS) for more realistic
shadow penumbra rendering. PCSS also uses a vogel-disk shaped kernel.

Additionally, both shadow-mapping techniques rotate the kernel on a per-pixel
basis to help soften under-sampling artifacts.

Temporal antialiasing
~~~~~~~~~~~~~~~~~~~~~

.. note::

    Available in Forward+.

Godot uses a custom TAA implementation based on the old TAA implementation from
`Spartan Engine <https://github.com/PanosK92/SpartanEngine>`__.

Temporal antialiasing requires motion vectors to work. If motion vectors
are not correctly generated, ghosting will occur when the camera or objects move.

Motion vectors are generated on the GPU in the main material shader. This is
done by running the vertex shader corresponding to the previous rendered frame
(with the previous camera transform) in addition to the vertex shader for the
current rendered frame, then storing the difference between them in a color buffer.

Alternatively, FSR 2.2 can be used as an upscaling solution that also provides
its own temporal antialiasing algorithm. FSR 2.2 is implemented on top of the
RenderingDevice abstraction as opposed to using AMD's reference code directly.

**TAA resolve:**

- `servers/rendering/renderer_rd/shaders/effects/taa_resolve.glsl <https://github.com/godotengine/godot/blob/4.6/servers/rendering/renderer_rd/shaders/effects/taa_resolve.glsl>`__

**FSR 2.2:**

- `servers/rendering/renderer_rd/effects/fsr2.cpp <https://github.com/godotengine/godot/blob/4.6/servers/rendering/renderer_rd/effects/fsr2.cpp>`__
- `servers/rendering/renderer_rd/shaders/effects/fsr2/ <https://github.com/godotengine/godot/tree/master/servers/rendering/renderer_rd/shaders/effects/fsr2>`__
- `thirdparty/amd-fsr2/ <https://github.com/godotengine/godot/tree/master/thirdparty/amd-fsr2>`__

Global illumination
~~~~~~~~~~~~~~~~~~~

.. note::

    VoxelGI and SDFGI use Forward+. LightmapGI baking requires a supported
    RenderingDevice and compute shaders, and runs in the editor.

Godot supports voxel-based GI (VoxelGI), signed distance field GI (SDFGI) and
lightmap baking and rendering (LightmapGI). These techniques can be used
simultaneously if desired.

Lightmap baking happens on the GPU using Vulkan compute shaders. The GPU-based
lightmapper is implemented in the LightmapperRD class, which inherits from the
Lightmapper class. This allows for implementing additional lightmappers, paving
the way for a future port of the CPU-based lightmapper present in Godot 3.x.
A CPU-based lightmapper is not provided by the current GPU implementation.

**Core GI C++ code:**

- `servers/rendering/renderer_rd/environment/gi.cpp <https://github.com/godotengine/godot/blob/4.6/servers/rendering/renderer_rd/environment/gi.cpp>`__
- `scene/3d/voxel_gi.cpp <https://github.com/godotengine/godot/blob/4.6/scene/3d/voxel_gi.cpp>`__ - VoxelGI node
- `editor/scene/3d/voxel_gi_editor_plugin.cpp <https://github.com/godotengine/godot/blob/4.6/editor/scene/3d/voxel_gi_editor_plugin.cpp>`__ - Editor UI for the VoxelGI node

**Core GI GLSL shaders:**

- `servers/rendering/renderer_rd/shaders/environment/voxel_gi.glsl <https://github.com/godotengine/godot/blob/4.6/servers/rendering/renderer_rd/shaders/environment/voxel_gi.glsl>`__
- `servers/rendering/renderer_rd/shaders/environment/voxel_gi_debug.glsl <https://github.com/godotengine/godot/blob/4.6/servers/rendering/renderer_rd/shaders/environment/voxel_gi_debug.glsl>`__ - VoxelGI debug draw mode
- `servers/rendering/renderer_rd/shaders/environment/sdfgi_debug.glsl <https://github.com/godotengine/godot/blob/4.6/servers/rendering/renderer_rd/shaders/environment/sdfgi_debug.glsl>`__ - SDFGI Cascades debug draw mode
- `servers/rendering/renderer_rd/shaders/environment/sdfgi_debug_probes.glsl <https://github.com/godotengine/godot/blob/4.6/servers/rendering/renderer_rd/shaders/environment/sdfgi_debug_probes.glsl>`__ - SDFGI Probes debug draw mode
- `servers/rendering/renderer_rd/shaders/environment/sdfgi_integrate.glsl <https://github.com/godotengine/godot/blob/4.6/servers/rendering/renderer_rd/shaders/environment/sdfgi_integrate.glsl>`__
- `servers/rendering/renderer_rd/shaders/environment/sdfgi_preprocess.glsl <https://github.com/godotengine/godot/blob/4.6/servers/rendering/renderer_rd/shaders/environment/sdfgi_preprocess.glsl>`__
- `servers/rendering/renderer_rd/shaders/environment/sdfgi_direct_light.glsl <https://github.com/godotengine/godot/blob/4.6/servers/rendering/renderer_rd/shaders/environment/sdfgi_direct_light.glsl>`__

**Lightmapper C++ code:**

- `scene/3d/lightmap_gi.cpp <https://github.com/godotengine/godot/blob/4.6/scene/3d/lightmap_gi.cpp>`__ - LightmapGI node
- `editor/scene/3d/lightmap_gi_editor_plugin.cpp <https://github.com/godotengine/godot/blob/4.6/editor/scene/3d/lightmap_gi_editor_plugin.cpp>`__ - Editor UI for the LightmapGI node
- `scene/3d/lightmapper.cpp <https://github.com/godotengine/godot/blob/4.6/scene/3d/lightmapper.cpp>`__ - Abstract class
- `modules/lightmapper_rd/lightmapper_rd.cpp <https://github.com/godotengine/godot/blob/4.6/modules/lightmapper_rd/lightmapper_rd.cpp>`__ - GPU-based lightmapper implementation

**Lightmapper GLSL shaders:**

- `modules/lightmapper_rd/lm_raster.glsl <https://github.com/godotengine/godot/blob/4.6/modules/lightmapper_rd/lm_raster.glsl>`__
- `modules/lightmapper_rd/lm_compute.glsl <https://github.com/godotengine/godot/blob/4.6/modules/lightmapper_rd/lm_compute.glsl>`__
- `modules/lightmapper_rd/lm_blendseams.glsl <https://github.com/godotengine/godot/blob/4.6/modules/lightmapper_rd/lm_blendseams.glsl>`__

Depth of field
~~~~~~~~~~~~~~

Depth of field is performed using a compute shader in Forward+.

Box, hexagon and circle bokeh shapes are available (from fastest to slowest).
Depth of field can optionally be jittered every frame to improve its appearance
when temporal antialiasing is enabled.

**Depth of field C++ code:**

- `servers/rendering/renderer_rd/effects/bokeh_dof.cpp <https://github.com/godotengine/godot/blob/4.6/servers/rendering/renderer_rd/effects/bokeh_dof.cpp>`__

**Depth of field GLSL shader (compute - used for Forward+):**

- `servers/rendering/renderer_rd/shaders/effects/bokeh_dof.glsl <https://github.com/godotengine/godot/blob/4.6/servers/rendering/renderer_rd/shaders/effects/bokeh_dof.glsl>`__


Screen-space effects (SSAO, SSIL, SSR, SSS)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. note::

    Available in Forward+.

The Forward+ renderer supports screen-space ambient occlusion,
screen-space indirect lighting, screen-space reflections and subsurface scattering.

SSAO uses an implementation derived from Intel's
`ASSAO <https://www.intel.com/content/www/us/en/developer/articles/technical/adaptive-screen-space-ambient-occlusion.html>`__
(converted to Vulkan). SSIL is derived from SSAO to provide high-performance
indirect lighting.

When both SSAO and SSIL are enabled, parts of SSAO and SSIL are shared to reduce
the performance impact.

SSAO, SSIL, and SSR are performed at half resolution by default to improve performance.

SSR makes use of a Hi-Z buffer to improve performance. This Hi-Z buffer is generated
from the depth buffer in a compute shader. See the
`pull request that overhauled SSR <https://github.com/godotengine/godot/pull/111210>`__
for more information.

**Screen-space effects C++ code:**

- `servers/rendering/renderer_rd/effects/ss_effects.cpp <https://github.com/godotengine/godot/blob/4.6/servers/rendering/renderer_rd/effects/ss_effects.cpp>`__

**Screen-space ambient occlusion GLSL shader:**

- `servers/rendering/renderer_rd/shaders/effects/ssao.glsl <https://github.com/godotengine/godot/blob/4.6/servers/rendering/renderer_rd/shaders/effects/ssao.glsl>`__
- `servers/rendering/renderer_rd/shaders/effects/ssao_blur.glsl <https://github.com/godotengine/godot/blob/4.6/servers/rendering/renderer_rd/shaders/effects/ssao_blur.glsl>`__
- `servers/rendering/renderer_rd/shaders/effects/ssao_interleave.glsl <https://github.com/godotengine/godot/blob/4.6/servers/rendering/renderer_rd/shaders/effects/ssao_interleave.glsl>`__
- `servers/rendering/renderer_rd/shaders/effects/ssao_importance_map.glsl <https://github.com/godotengine/godot/blob/4.6/servers/rendering/renderer_rd/shaders/effects/ssao_importance_map.glsl>`__

**Screen-space indirect lighting GLSL shader:**

- `servers/rendering/renderer_rd/shaders/effects/ssil.glsl <https://github.com/godotengine/godot/blob/4.6/servers/rendering/renderer_rd/shaders/effects/ssil.glsl>`__
- `servers/rendering/renderer_rd/shaders/effects/ssil_blur.glsl <https://github.com/godotengine/godot/blob/4.6/servers/rendering/renderer_rd/shaders/effects/ssil_blur.glsl>`__
- `servers/rendering/renderer_rd/shaders/effects/ssil_interleave.glsl <https://github.com/godotengine/godot/blob/4.6/servers/rendering/renderer_rd/shaders/effects/ssil_interleave.glsl>`__
- `servers/rendering/renderer_rd/shaders/effects/ssil_importance_map.glsl <https://github.com/godotengine/godot/blob/4.6/servers/rendering/renderer_rd/shaders/effects/ssil_importance_map.glsl>`__

**Screen-space reflections GLSL shader:**

- `servers/rendering/renderer_rd/shaders/effects/screen_space_reflection.glsl <https://github.com/godotengine/godot/blob/4.6/servers/rendering/renderer_rd/shaders/effects/screen_space_reflection.glsl>`__
- `servers/rendering/renderer_rd/shaders/effects/screen_space_reflection_filter.glsl <https://github.com/godotengine/godot/blob/4.6/servers/rendering/renderer_rd/shaders/effects/screen_space_reflection_filter.glsl>`__
- `servers/rendering/renderer_rd/shaders/effects/screen_space_reflection_resolve.glsl <https://github.com/godotengine/godot/blob/4.6/servers/rendering/renderer_rd/shaders/effects/screen_space_reflection_resolve.glsl>`__
- `servers/rendering/renderer_rd/shaders/effects/screen_space_reflection_hiz.glsl <https://github.com/godotengine/godot/blob/4.6/servers/rendering/renderer_rd/shaders/effects/screen_space_reflection_hiz.glsl>`__
- `servers/rendering/renderer_rd/shaders/effects/screen_space_reflection_downsample.glsl <https://github.com/godotengine/godot/blob/4.6/servers/rendering/renderer_rd/shaders/effects/screen_space_reflection_downsample.glsl>`__

**Subsurface scattering GLSL:**

- `servers/rendering/renderer_rd/shaders/effects/subsurface_scattering.glsl <https://github.com/godotengine/godot/blob/4.6/servers/rendering/renderer_rd/shaders/effects/subsurface_scattering.glsl>`__

Sky rendering
~~~~~~~~~~~~~

.. seealso::

    :ref:`doc_sky_shader`

Godot supports using shaders to render the sky background. The radiance map
(which is used to provide ambient light and reflections for PBR materials) is
automatically updated based on the sky shader.

The SkyMaterial resources such as ProceduralSkyMaterial, PhysicalSkyMaterial and
PanoramaSkyMaterial generate a built-in shader for sky rendering. This is
similar to what BaseMaterial3D provides for 3D scene materials.

A detailed technical implementation can be found in the
`Custom sky shaders in Godot 4.0 <https://godotengine.org/article/custom-sky-shaders-godot-4-0>`__
article.

**Sky rendering C++ code:**

- `servers/rendering/renderer_rd/environment/sky.cpp <https://github.com/godotengine/godot/blob/4.6/servers/rendering/renderer_rd/environment/sky.cpp>`__ - Sky rendering
- `scene/resources/sky.cpp <https://github.com/godotengine/godot/blob/4.6/scene/resources/sky.cpp>`__ - Sky resource (not to be confused with sky rendering)
- `scene/resources/3d/sky_material.cpp <https://github.com/godotengine/godot/blob/4.6/scene/resources/3d/sky_material.cpp>`__ SkyMaterial resources (used in the Sky resource)

**Sky rendering GLSL shader:**

Volumetric fog
~~~~~~~~~~~~~~

.. note::

    Available in Forward+.

.. seealso::

    :ref:`doc_fog_shader`

Godot supports a frustum-aligned voxel (froxel) approach to volumetric fog
rendering. As opposed to a post-processing filter, this approach is more
general-purpose as it can work with any light type. Fog can also use shaders for
custom behavior, which allows animating the fog or using a 3D texture to
represent density.

The FogMaterial resource generates a built-in shader for FogVolume nodes. This is
similar to what BaseMaterial3D provides for 3D scene materials.

A detailed technical explanation can be found in the
`Fog Volumes arrive in Godot 4.0 <https://godotengine.org/article/fog-volumes-arrive-in-godot-4>`__
article.

**Volumetric fog C++ code:**

- `servers/rendering/renderer_rd/environment/fog.cpp <https://github.com/godotengine/godot/blob/4.6/servers/rendering/renderer_rd/environment/fog.cpp>`__ - General volumetric fog
- `scene/3d/fog_volume.cpp <https://github.com/godotengine/godot/blob/4.6/scene/3d/fog_volume.cpp>`__ - FogVolume node
- `scene/resources/3d/fog_material.cpp <https://github.com/godotengine/godot/blob/4.6/scene/resources/3d/fog_material.cpp>`__ - FogMaterial resource (used by FogVolume)

**Volumetric fog GLSL shaders:**

- `servers/rendering/renderer_rd/shaders/environment/volumetric_fog.glsl <https://github.com/godotengine/godot/blob/4.6/servers/rendering/renderer_rd/shaders/environment/volumetric_fog.glsl>`__
- `servers/rendering/renderer_rd/shaders/environment/volumetric_fog_process.glsl <https://github.com/godotengine/godot/blob/4.6/servers/rendering/renderer_rd/shaders/environment/volumetric_fog_process.glsl>`__

Occlusion culling
~~~~~~~~~~~~~~~~~

While modern GPUs can handle drawing a lot of triangles, the number of draw
calls in complex scenes can still be a bottleneck (even with Vulkan, Direct3D 12,
and Metal).

Godot 4 supports occlusion culling to reduce overdraw (when the depth prepass
is disabled) and reduce vertex throughput.
This is done by rasterizing a low-resolution buffer on the CPU using
`Embree <https://github.com/embree/embree>`__. The buffer's resolution depends
on the number of CPU threads on the system, as this is done in parallel.
This buffer includes occluder shapes that were baked in the editor or created at
runtime. The occlusion culling buffer is jittered by a small amount every frame
to help reduce under-sampling artifacts, which would lead to false positives
(objects getting occluded when they shouldn't be).

As complex occluders can introduce a lot of strain on the CPU, baked occluders
can be simplified automatically when generated in the editor.

Godot's occlusion culling doesn't support dynamic occluders yet, but
OccluderInstance3D nodes can still have their visibility toggled or be moved.
However, this will be slow when updating complex occluders this way. Therefore,
updating occluders at runtime is best done only on simple occluder shapes such
as quads or cuboids.

This CPU-based approach has a few advantages over other solutions, such as
portals and rooms or a GPU-based culling solution:

- No manual setup required (but can be tweaked manually for best performance).
- No frame delay, which is problematic in cutscenes during camera cuts or when
  the camera moves fast behind a wall.
- Works the same on all rendering drivers and methods, with no unpredictable
  behavior depending on the driver or GPU hardware.

Occlusion culling is performed by registering occluder meshes, which is done
using OccluderInstance3D *nodes* (which themselves use Occluder3D *resources*).
RenderingServer then performs occlusion culling by calling Embree in
RendererSceneOcclusionCull.

**Occlusion culling C++ code:**

- `scene/3d/occluder_instance_3d.cpp <https://github.com/godotengine/godot/blob/4.6/scene/3d/occluder_instance_3d.cpp>`__
- `servers/rendering/renderer_scene_occlusion_cull.cpp <https://github.com/godotengine/godot/blob/4.6/servers/rendering/renderer_scene_occlusion_cull.cpp>`__

Visibility range (LOD)
~~~~~~~~~~~~~~~~~~~~~~

Godot supports manually authored hierarchical level of detail (HLOD), with
distances specified by the user in the inspector.

In RenderingSceneCull, the ``_scene_cull()`` and ``_render_scene()`` functions
are where most of the LOD determination happens. Each viewport can render the
same mesh with different LODs (to allow for split screen rendering to look correct).

**Visibility range C++ code:**

- `servers/rendering/renderer_scene_cull.cpp <https://github.com/godotengine/godot/blob/4.6/servers/rendering/renderer_scene_cull.cpp>`__

Automatic mesh LOD
~~~~~~~~~~~~~~~~~~

The ImporterMesh class is used for the 3D mesh import workflow in the editor.
Its ``generate_lods()`` function handles generating using the
`meshoptimizer <https://meshoptimizer.org/>`__ library.

LOD mesh generation also generates shadow meshes at the same time. These are
meshes that have their vertices welded regardless of smoothing and materials.
This is used to improve shadow rendering performance by lowering the vertex
throughput required to render shadows.

The RenderingSceneCull class's ``_render_scene()`` function determines which
mesh LOD should be used when rendering. Each viewport can render the
same mesh with different LODs (to allow for split screen rendering to look correct).

The mesh LOD is automatically chosen based on a screen coverage metric. This
takes resolution and camera FOV changes into account without requiring user
intervention. The threshold multiplier can be adjusted in the project settings.

To improve performance, shadow rendering and reflection probe rendering also choose
their own mesh LOD thresholds (which can be different from the main scene rendering).

**Mesh LOD generation on import C++ code:**

- `scene/resources/3d/importer_mesh.cpp <https://github.com/godotengine/godot/blob/4.6/scene/resources/3d/importer_mesh.cpp>`__

**Mesh LOD determination C++ code:**

- `servers/rendering/renderer_scene_cull.cpp <https://github.com/godotengine/godot/blob/4.6/servers/rendering/renderer_scene_cull.cpp>`__
