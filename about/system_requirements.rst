:allow_comments: False

.. _doc_system_requirements:

System requirements
===================

Rendered EGP projects require Forward+ through a supported RenderingDevice
driver: Vulkan, Direct3D 12 or Metal, depending on the platform and build.
Compatibility and Mobile renderers, OpenGL/OpenGL ES and ANGLE are removed;
devices below Forward+ requirements have no fallback renderer. Browser
rendering, the Web editor and Web exports are unsupported. Headless servers
and tooling retain the dummy backend and can run without a GPU or display.

The tables below retain upstream Forward+ hardware guidance as estimates,
not measured EGP performance guarantees. Scene complexity, render settings
and native integrations affect requirements. Review :ref:`doc_egp_qualification`
and :ref:`doc_egp_getting_started` for tested revisions and platform limits.

Godot editor
------------

These are the **minimum** specifications required to run the Godot editor and work
on a simple 2D or 3D project:

Desktop or laptop PC - Minimum
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. When adjusting specifications, make sure to only mention hardware that can run the required OS version.
.. For example, the oldest Mac model that can run macOS 13 is the 2017 iMac,
.. so the x86 CPU requirement for macOS should not be set earlier than that.

+----------------------+-----------------------------------------------------------------------------------------+
| **CPU**              | - **Windows:** x86_32 CPU with SSE2 support, x86_64 CPU with SSE4.2 support, ARMv8 CPU  |
|                      |                                                                                         |
|                      |   - *Example: Intel Core 2 Duo E8200, AMD FX-4100, Snapdragon X Elite*                  |
|                      |                                                                                         |
|                      | - **macOS:** x86_64 or ARM CPU (Apple Silicon)                                          |
|                      |                                                                                         |
|                      |   - *Example: Intel 7th Gen (Kaby Lake) CPU, Apple M1*                                  |
|                      |                                                                                         |
|                      | - **Linux:** x86_32 CPU with SSE2 support, x86_64 CPU with SSE4.2 support, ARMv7 or     |
|                      |   ARMv8 CPU                                                                             |
|                      |                                                                                         |
|                      |   - *Example: Intel Core 2 Duo E8200, AMD FX-4100, Raspberry Pi 4*                      |
+----------------------+-----------------------------------------------------------------------------------------+
| **GPU**              | - **Forward+ renderer:** Integrated graphics with full Vulkan 1.0 support               |
|                      |                                                                                         |
|                      |   - *Example: Intel HD Graphics 510 (Skylake), AMD Radeon R5 Graphics (Kaveri)*         |
|                      |                                                                                         |
+----------------------+-----------------------------------------------------------------------------------------+
| **RAM**              | - **Native editor:** 4 GB                                                               |
+----------------------+-----------------------------------------------------------------------------------------+
| **Storage**          | 200 MB (used for the executable, project files, and cache).                             |
|                      | Exporting projects requires downloading export templates separately                     |
|                      | (up to 1.5 GB after installation, depending on the target platforms chosen).            |
+----------------------+-----------------------------------------------------------------------------------------+
| **Operating system** | - **Native editor:** Windows 10, macOS 12 (Intel Macs), macOS 13 (Apple Silicon Macs),  |
|                      |   Linux distribution released after 2018                                                |
+----------------------+-----------------------------------------------------------------------------------------+

.. note::

    If your x86_64 CPU does not support SSE4.2, you can still run the 32-bit Godot
    executable which only has a SSE2 requirement (all x86_64 CPUs support SSE2).

    While supported on Linux, we have no official minimum requirements for running on
    rv64 (RISC-V), ppc64 & ppc32 (PowerPC), and loongarch64. In addition you must
    compile the editor for that platform (as well as export templates) yourself,
    no official downloads are currently provided. RISC-V compiling instructions can
    be found on the :ref:`doc_compiling_for_linuxbsd` page.

Mobile device (smartphone/tablet) - Minimum
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

+----------------------+-----------------------------------------------------------------------------------------+
| **CPU**              | - **Android:** SoC with any 32-bit or 64-bit ARM or x86 CPU                             |
|                      |                                                                                         |
|                      |   - *Example: Qualcomm Snapdragon 430, Samsung Exynos 5 Octa 5430*                      |
|                      |                                                                                         |
|                      | - **iOS:** *Cannot run the editor*                                                      |
+----------------------+-----------------------------------------------------------------------------------------+
| **GPU**              | - **Forward+ renderer:** SoC featuring GPU with full Vulkan 1.0 support                 |
|                      |                                                                                         |
|                      |   - *Example: Qualcomm Adreno 505, Mali-G71 MP2*                                        |
|                      |                                                                                         |
+----------------------+-----------------------------------------------------------------------------------------+
| **RAM**              | - **Native editor:** 3 GB                                                               |
+----------------------+-----------------------------------------------------------------------------------------+
| **Storage**          | 200 MB (used for the executable, project files, and cache).                             |
|                      | Exporting projects requires downloading export templates separately                     |
|                      | (up to 1.5 GB after installation, depending on the target platforms chosen).            |
+----------------------+-----------------------------------------------------------------------------------------+
| **Operating system** | - **Native editor:** Android 9.0                                                        |
+----------------------+-----------------------------------------------------------------------------------------+

These are the **recommended** specifications to get a smooth experience with the
Godot editor on a simple 2D or 3D project:

Desktop or laptop PC - Recommended
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

+----------------------+---------------------------------------------------------------------------------------------+
| **CPU**              | - **Windows:** x86_64 CPU with SSE4.2 support, with 4 physical cores or more, ARMv8 CPU     |
|                      |                                                                                             |
|                      |   - *Example: Intel Core i5-6600K, AMD Ryzen 5 1600, Snapdragon X Elite*                    |
|                      |                                                                                             |
|                      | - **macOS:** x86_64 or ARM CPU (Apple Silicon)                                              |
|                      |                                                                                             |
|                      |   - *Example: Intel Core i5-8500, Apple M1*                                                 |
|                      |                                                                                             |
|                      | - **Linux:** x86_64 CPU with SSE4.2 support, ARMv7 or ARMv8 CPU                             |
|                      |                                                                                             |
|                      |   - *Example: Intel Core i5-6600K, AMD Ryzen 5 1600, Raspberry Pi 5 with overclocking*      |
+----------------------+---------------------------------------------------------------------------------------------+
| **GPU**              | - **Forward+ renderer:** Dedicated graphics with full Vulkan 1.2 support                    |
|                      |                                                                                             |
|                      |   - *Example: NVIDIA GeForce GTX 1050 (Pascal), AMD Radeon RX 460 (GCN 4.0)*                |
|                      |                                                                                             |
+----------------------+---------------------------------------------------------------------------------------------+
| **RAM**              | - **Native editor:** 8 GB                                                                   |
+----------------------+---------------------------------------------------------------------------------------------+
| **Storage**          | 2 GB (used for the executable, project files, all export templates, and cache)              |
+----------------------+---------------------------------------------------------------------------------------------+
| **Operating system** | - **Native editor:** Windows 11, macOS 14, Linux distribution released after 2020           |
+----------------------+---------------------------------------------------------------------------------------------+

Mobile device (smartphone/tablet) - Recommended
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

+----------------------+-----------------------------------------------------------------------------------------+
| **CPU**              | - **Android:** SoC with 64-bit ARM or x86 CPU, with 3 "performance" cores or more       |
|                      |                                                                                         |
|                      |   - *Example: Qualcomm Snapdragon 845, Samsung Exynos 9810*                             |
|                      |                                                                                         |
|                      | - **iOS:** *Cannot run the editor*                                                      |
+----------------------+-----------------------------------------------------------------------------------------+
| **GPU**              | - **Forward+ renderer:** SoC featuring GPU with full Vulkan 1.2 support                 |
|                      |                                                                                         |
|                      |   - *Example: Qualcomm Adreno 630, Mali-G72 MP18*                                       |
|                      |                                                                                         |
+----------------------+-----------------------------------------------------------------------------------------+
| **RAM**              | - **Native editor:** 6 GB                                                               |
+----------------------+-----------------------------------------------------------------------------------------+
| **Storage**          | 2 GB (used for the executable, project files, all export templates, and cache)          |
+----------------------+-----------------------------------------------------------------------------------------+
| **Operating system** | - **Native editor:** Android 11.0                                                       |
+----------------------+-----------------------------------------------------------------------------------------+

Exported Godot project
----------------------

.. warning::

    The requirements below are a baseline for a **simple** 2D or 3D project,
    with basic scripting and few visual flourishes. CPU, GPU, RAM and
    storage requirements will heavily vary depending on your project's scope,
    its renderer, viewport resolution and graphics settings chosen.
    Other programs running on the system while the project is running
    will also compete for resources, including RAM and video RAM.

    It is strongly recommended to do your own testing on low-end hardware to
    make sure your project runs at the desired speed. To provide scalability for
    low-end hardware, you will also need to introduce a
    `graphics options menu <https://github.com/godotengine/godot-demo-projects/tree/master/3d/graphics_settings>`__
    to your project.

These are the **minimum** specifications required to run a simple 2D or 3D
project exported with Godot:

Desktop or laptop PC - Minimum
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. When adjusting specifications, make sure to only mention hardware that can run the required OS version.
.. For example, the oldest Mac model that can run macOS 13 is the 2017 iMac,
.. so the x86 CPU requirement for macOS should not be set earlier than that.

+----------------------+-----------------------------------------------------------------------------------------+
| **CPU**              | - **Windows:** x86_32 CPU with SSE2 support, x86_64 CPU with SSE4.2 support,            |
|                      |   ARMv8 CPU                                                                             |
|                      |                                                                                         |
|                      |   - *Example: Intel Core 2 Duo E8200, AMD FX-4100, Snapdragon X Elite*                  |
|                      |                                                                                         |
|                      | - **macOS:** x86_64 or ARM CPU (Apple Silicon)                                          |
|                      |                                                                                         |
|                      |   - *Example: Intel 7th Gen (Kaby Lake) CPU, Apple M1*                                  |
|                      |                                                                                         |
|                      | - **Linux:** x86_32 CPU with SSE2 support, x86_64 CPU with SSE4.2 support,              |
|                      |   ARMv7 or ARMv8 CPU                                                                    |
|                      |                                                                                         |
|                      |   - *Example: Intel Core 2 Duo E8200, AMD FX-4100, Raspberry Pi 4*                      |
+----------------------+-----------------------------------------------------------------------------------------+
| **GPU**              | - **Forward+ renderer:** Integrated graphics with full Vulkan 1.0 support,              |
|                      |   Metal 3 support (macOS) or Direct3D 12 (12_0 feature level) support (Windows)         |
|                      |                                                                                         |
|                      |   - *Example: Intel HD Graphics 510 (Skylake), AMD Radeon R5 Graphics (Kaveri)*         |
|                      |                                                                                         |
+----------------------+-----------------------------------------------------------------------------------------+
| **RAM**              | - **For native exports:** 2 GB                                                          |
+----------------------+-----------------------------------------------------------------------------------------+
| **Storage**          | 150 MB (used for the executable, project files, and cache)                              |
+----------------------+-----------------------------------------------------------------------------------------+
| **Operating system** | - **For native exports:** Windows 10, macOS 12 (Intel Macs), macOS 13 (Apple Silicon    |
|                      |   Macs), Linux distribution released after 2018                                         |
+----------------------+-----------------------------------------------------------------------------------------+

Mobile device (smartphone/tablet) - Minimum
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

+----------------------+-----------------------------------------------------------------------------------------+
| **CPU**              | - **Android:** SoC with any 32-bit or 64-bit ARM or x86 CPU                             |
|                      |                                                                                         |
|                      |   - *Example: Qualcomm Snapdragon 430, Samsung Exynos 5 Octa 5430*                      |
|                      |                                                                                         |
|                      | - **iOS:** SoC with 64-bit ARM CPU                                                      |
|                      |                                                                                         |
|                      |   - *Example: Apple A9 (iPhone 6S)*                                                     |
+----------------------+-----------------------------------------------------------------------------------------+
| **GPU**              | - **Forward+ renderer:** SoC featuring GPU with full Vulkan 1.0 support, or             |
|                      |   Metal 3 support (iOS/iPadOS)                                                          |
|                      |                                                                                         |
|                      | - *Example (Vulkan): Qualcomm Adreno 505, Mali-G71 MP2, Apple A12 (iPhone XR/XS)*       |
|                      | - *Example (Metal): Apple A12 (iPhone XR/XS)*                                           |
|                      |                                                                                         |
+----------------------+-----------------------------------------------------------------------------------------+
| **RAM**              | - **For native exports:** 1 GB                                                          |
+----------------------+-----------------------------------------------------------------------------------------+
| **Storage**          | 150 MB (used for the executable, project files, and cache)                              |
+----------------------+-----------------------------------------------------------------------------------------+
| **Operating system** | - **For native exports:** Android 9.0,                                                  |
|                      |   iOS 15.0 (with Vulkan), iOS 16.0 (with Metal)                                         |
+----------------------+-----------------------------------------------------------------------------------------+

These are the **recommended** specifications to get a smooth experience with a
simple 2D or 3D project exported with Godot:

Desktop or laptop PC - Recommended
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

+----------------------+----------------------------------------------------------------------------------------------+
| **CPU**              | - **Windows:** x86_64 CPU with SSE4.2 support, with 4 physical cores or more, ARMv8 CPU      |
|                      |                                                                                              |
|                      |   - *Example: Intel Core i5-6600K, AMD Ryzen 5 1600, Snapdragon X Elite*                     |
|                      |                                                                                              |
|                      | - **macOS:** x86_64 or ARM CPU (Apple Silicon)                                               |
|                      |                                                                                              |
|                      |   - *Example: Intel Core i5-8500, Apple M1*                                                  |
|                      |                                                                                              |
|                      | - **Linux:** x86_64 CPU with SSE4.2 support, with 4 physical cores or more,                  |
|                      |   ARMv7 or ARMv8 CPU                                                                         |
|                      |                                                                                              |
|                      |   - *Example: Intel Core i5-6600K, AMD Ryzen 5 1600, Raspberry Pi 5 with overclocking*       |
+----------------------+----------------------------------------------------------------------------------------------+
| **GPU**              | - **Forward+ renderer:** Dedicated graphics with full Vulkan 1.2 support,                    |
|                      |   Metal 3 support (macOS), or Direct3D 12 (12_0 feature level) support (Windows)             |
|                      |                                                                                              |
|                      |   - *Example: NVIDIA GeForce GTX 1050 (Pascal), AMD Radeon RX 460 (GCN 4.0)*                 |
|                      |                                                                                              |
+----------------------+----------------------------------------------------------------------------------------------+
| **RAM**              | - **For native exports:** 4 GB                                                               |
+----------------------+----------------------------------------------------------------------------------------------+
| **Storage**          | 150 MB (used for the executable, project files, and cache)                                   |
+----------------------+----------------------------------------------------------------------------------------------+
| **Operating system** | - **For native exports:** Windows 11, macOS 14, Linux distribution released after 2020       |
+----------------------+----------------------------------------------------------------------------------------------+

Mobile device (smartphone/tablet) - Recommended
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

+----------------------+-----------------------------------------------------------------------------------------+
| **CPU**              | - **Android:** SoC with 64-bit ARM or x86 CPU, with 3 "performance" cores or more       |
|                      |                                                                                         |
|                      |   - *Example: Qualcomm Snapdragon 845, Samsung Exynos 9810*                             |
|                      |                                                                                         |
|                      | - **iOS:** SoC with 64-bit ARM CPU                                                      |
|                      |                                                                                         |
|                      |   - *Example: Apple A14 (iPhone 12)*                                                    |
+----------------------+-----------------------------------------------------------------------------------------+
| **GPU**              | - **Forward+ renderer:** SoC featuring GPU with full Vulkan 1.2 support, or             |
|                      |   Metal 3 support (iOS/iPadOS)                                                          |
|                      |                                                                                         |
|                      |   - *Example: Qualcomm Adreno 630, Mali-G72 MP18, Apple A14 (iPhone 12)*                |
|                      |                                                                                         |
+----------------------+-----------------------------------------------------------------------------------------+
| **RAM**              | - **For native exports:** 2 GB                                                          |
+----------------------+-----------------------------------------------------------------------------------------+
| **Storage**          | 150 MB (used for the executable, project files, and cache)                              |
+----------------------+-----------------------------------------------------------------------------------------+
| **Operating system** | - **For native exports:** Android 9.0, iOS 16.0                                         |
+----------------------+-----------------------------------------------------------------------------------------+
