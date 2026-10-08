.. _doc_godot_cpp_getting_started:

Getting started
===============

Workflow overview
-----------------

The EGP C++ editor tools create and build extensions against the SDK embedded
in your engine. This keeps generated bindings, method hashes and compatibility
metadata aligned with the exact engine API.

Setting up the project
----------------------

Install a C++ compiler and xmake 3.1.1. Open your project in EGP, create an
extension in the C++ panel, and extract its matching SDK for command-line builds.
Keep that SDK separate from your extension sources. This tutorial uses
``gdextension_cpp_example/src`` for code, ``project`` for the test game, and an
absolute SDK path supplied through ``--egp_cpp_sdk``.

The generated extension includes ``xmake.lua`` and a ``.gdextension`` descriptor.
Use the engine's matching SDK rather than an upstream SDK snapshot: fork-specific
classes and method signatures require matching bindings.

Creating a simple plugin
------------------------

Now it's time to build an actual plugin. We'll start by creating an empty Godot
project in which we'll place a few files.

Open Godot and create a new project. For this example, we will place it in a
folder called ``project`` inside our GDExtension's folder structure.

In our project, we'll create a scene containing a Node called "Main" and
we'll save it as ``main.tscn``. We'll come back to that later.

Back in the top-level GDExtension module folder, we're also going to create a
subfolder called ``src`` in which we'll place our source files.

You should now have ``project`` and ``src`` directories in your extension.

Your folder structure should now look like this:

.. code-block:: none

    gdextension_cpp_example/
    |
    +--project/                  # game example/demo to test the extension
    |
    +--sdk/             # C++ bindings
    |
    +--src/                   # source code of the extension we are building

In the ``src`` folder, we'll start with creating our header file for the
GDExtension node we'll be creating. We will name it ``gdexample.h``:

.. code-block:: cpp
    :caption: gdextension_cpp_example/src/gdexample.h

    #pragma once

    #include <godot_cpp/classes/sprite2d.hpp>

    namespace godot {

    class GDExample : public Sprite2D {
        GDCLASS(GDExample, Sprite2D)

    private:
        double time_passed;

    protected:
        static void _bind_methods();

    public:
        GDExample();
        ~GDExample();

        void _process(double delta) override;
    };

    } // namespace godot

There are a few things of note to the above. We include ``sprite2d.hpp`` which
contains bindings to the Sprite2D class. We'll be extending this class in our
module.

We're using the namespace ``godot``, since everything in GDExtension is defined
within this namespace.

Then we have our class definition, which inherits from our Sprite2D through a
container class. We'll see a few side effects of this later on. The
``GDCLASS`` macro sets up a few internal things for us.

After that, we declare a single member variable called ``time_passed``.

In the next block we're defining our methods, we have our constructor
and destructor defined, but there are two other functions that will likely look
familiar to some, and one new method.

The first is ``_bind_methods``, which is a static function that Godot will
call to find out which methods can be called and which properties it exposes.
The second is our ``_process`` function, which will work exactly the same
as the ``_process`` function you're used to in GDScript.

Let's implement our functions by creating our ``gdexample.cpp`` file:

.. code-block:: cpp
    :caption: gdextension_cpp_example/src/gdexample.cpp

    #include "gdexample.h"
    #include <godot_cpp/core/class_db.hpp>

    using namespace godot;

    void GDExample::_bind_methods() {
    }

    GDExample::GDExample() {
        // Initialize any variables here.
        time_passed = 0.0;
    }

    GDExample::~GDExample() {
        // Add your cleanup here.
    }

    void GDExample::_process(double delta) {
        time_passed += delta;

        Vector2 new_position = Vector2(10.0 + (10.0 * sin(time_passed * 2.0)), 10.0 + (10.0 * cos(time_passed * 1.5)));

        set_position(new_position);
    }

This one should be straightforward. We're implementing each method of our class
that we defined in our header file.

Note our ``_process`` function, which keeps track of how much time has passed
and calculates a new position for our sprite using a sine and cosine function.

There is one more C++ file we need; we'll name it ``register_types.cpp``. Our
GDExtension plugin can contain multiple classes, each with their own header
and source file like we've implemented ``GDExample`` up above. What we need now
is a small bit of code that tells Godot about all the classes in our
GDExtension plugin.

.. code-block:: cpp
    :caption: gdextension_cpp_example/src/register_types.cpp

    #include "register_types.h"

    #include "gdexample.h"

    #include <gdextension_interface.h>
    #include <godot_cpp/core/defs.hpp>
    #include <godot_cpp/godot.hpp>

    using namespace godot;

    void initialize_example_module(ModuleInitializationLevel p_level) {
        if (p_level != MODULE_INITIALIZATION_LEVEL_SCENE) {
            return;
        }

        GDREGISTER_CLASS(GDExample);
    }

    void uninitialize_example_module(ModuleInitializationLevel p_level) {
        if (p_level != MODULE_INITIALIZATION_LEVEL_SCENE) {
            return;
        }
    }

    extern "C" {
    // Initialization.
    GDExtensionBool GDE_EXPORT example_library_init(GDExtensionInterfaceGetProcAddress p_get_proc_address, const GDExtensionClassLibraryPtr p_library, GDExtensionInitialization *r_initialization) {
        godot::GDExtensionBinding::InitObject init_obj(p_get_proc_address, p_library, r_initialization);

        init_obj.register_initializer(initialize_example_module);
        init_obj.register_terminator(uninitialize_example_module);
        init_obj.set_minimum_library_initialization_level(MODULE_INITIALIZATION_LEVEL_SCENE);

        return init_obj.init();
    }
    }

The ``initialize_example_module`` and ``uninitialize_example_module`` functions get
called respectively when Godot loads our plugin and when it unloads it. All
we're doing here is parse through the functions in our bindings module to
initialize them, but you might have to set up more things depending on your
needs. We call the ``GDREGISTER_CLASS`` macro for each of our classes in our library.

.. note::

    You can find information about ``GDREGISTER_CLASS`` (and alternatives) at :ref:`doc_object_class`.

The important function is the third function called ``example_library_init``.
We first call a function in our bindings library that creates an initialization object.
This object registers the initialization and termination functions of the GDExtension.
Furthermore, it sets the level of initialization (core, servers, scene, editor, level).

At last, we need the header file for the ``register_types.cpp`` named
``register_types.h``.

.. code-block:: cpp
    :caption: gdextension_cpp_example/src/register_types.h

    #pragma once

    #include <godot_cpp/core/class_db.hpp>

    using namespace godot;

    void initialize_example_module(ModuleInitializationLevel p_level);
    void uninitialize_example_module(ModuleInitializationLevel p_level);

Compiling the plugin
--------------------

Use the matching pre-generated SDK from EGP's editor. Create an ``xmake.lua``
project using :doc:`the native extension workflow </egp/cpp_extensions>`.
The tutorial's C++ implementation files remain under ``src/``; configure the
shared-library basename and output directory to match the descriptor below.

A standalone project can include the SDK directly:

.. code-block:: lua

    add_rules("mode.debug", "mode.release")
    option("egp_cpp_sdk") set_showmenu(true) option_end()
    local sdk = get_config("egp_cpp_sdk")
    if sdk then includes(path.join(sdk, "xmake.lua")) end
    target("extension")
        set_kind("shared")
        set_languages("cxx17")
        if is_plat("windows") then
            set_runtimes(is_mode("debug") and "MDd" or "MD")
            set_prefixname("")
        else
            set_prefixname("lib")
        end
        local platform = is_plat("macosx") and "macos" or get_config("plat")
        local architecture = get_config("arch") == "x64" and "x86_64" or get_config("arch")
        local mode = is_mode("debug") and "template_debug" or "template_release"
        local suffix = is_plat("macosx") and "" or "." .. architecture
        set_basename("gdexample." .. platform .. "." .. mode .. suffix)
        set_targetdir("project/bin")
        add_files("src/*.cpp")
        add_includedirs("src")
        add_deps("godot-cpp")
    target_end()

From this extension directory, run:

.. code-block:: shell

    xmake f --egp_cpp_sdk=/absolute/matching-sdk -p windows -a x64 -m debug
    xmake -b extension

Choose the actual target platform/architecture and ``release`` mode when building
another variant. The descriptor's filenames must agree with the shared libraries
published under ``project/bin``. Test against the matching EGP editor and export
templates; use the editor's Reload action only at a supported runtime boundary.

Using the GDExtension module
----------------------------

Before we jump back into Godot, we need to create one more file in
``project/bin/``.

This file lets Godot know what dynamic libraries should be
loaded for each platform and the entry function for the module. It is called ``gdexample.gdextension``.

.. code-block:: none

    [configuration]

    entry_symbol = "example_library_init"
    compatibility_minimum = "4.1"
    reloadable = true

    [libraries]

    macos.debug = "./libgdexample.macos.template_debug.dylib"
    macos.release = "./libgdexample.macos.template_release.dylib"
    windows.debug.x86_32 = "./gdexample.windows.template_debug.x86_32.dll"
    windows.release.x86_32 = "./gdexample.windows.template_release.x86_32.dll"
    windows.debug.x86_64 = "./gdexample.windows.template_debug.x86_64.dll"
    windows.release.x86_64 = "./gdexample.windows.template_release.x86_64.dll"
    linux.debug.x86_64 = "./libgdexample.linux.template_debug.x86_64.so"
    linux.release.x86_64 = "./libgdexample.linux.template_release.x86_64.so"
    linux.debug.arm64 = "./libgdexample.linux.template_debug.arm64.so"
    linux.release.arm64 = "./libgdexample.linux.template_release.arm64.so"
    linux.debug.rv64 = "./libgdexample.linux.template_debug.rv64.so"
    linux.release.rv64 = "./libgdexample.linux.template_release.rv64.so"

This file contains a ``configuration`` section that controls the entry function of the module.
You should also set the minimum compatible Godot version with ``compatibility_minimum``,
which prevents older version of Godot from trying to load your extension.
The ``reloadable`` flag enables automatic reloading of your extension by the editor every time you recompile it,
without needing to restart the editor. This only works if you compile your extension in debug mode (default).

The ``libraries`` section is the important bit: it tells Godot the location of the
dynamic library in the project's filesystem for each supported platform. It will
also result in *just* that file being exported when you export the project,
which means the data pack won't contain libraries that are incompatible with the
target platform.

You can learn more about ``.gdextension`` files at :ref:`doc_gdextension_file`.

Here is another overview to check the correct file structure:

.. code-block:: none

    gdextension_cpp_example/
    |
    +--project/                  # game example/demo to test the extension
    |   |
    |   +--main.tscn
    |   |
    |   +--bin/
    |       |
    |       +--gdexample.gdextension
    |
    +--sdk/             # C++ bindings
    |
    +--src/                   # source code of the extension we are building
    |   |
    |   +--register_types.cpp
    |   +--register_types.h
    |   +--gdexample.cpp
    |   +--gdexample.h

Time to jump back into Godot. We load up the main scene we created way back in
the beginning and now add a newly available GDExample node to the scene:

.. image:: img/gdextension_cpp_nodes.webp

We're going to assign the Godot logo to this node as our texture, disable the
``centered`` property:

.. image:: img/gdextension_cpp_sprite.webp

We're finally ready to run the project:

.. video:: img/gdextension_cpp_animated.webm
   :alt: Screen recording of a game window, with Godot logo moving in the top-left corner
   :autoplay:
   :loop:
   :muted:
   :align: default

Adding properties
-----------------

GDScript allows you to add properties to your script using the ``export``
keyword. In GDExtension you have to register the properties with a getter and
setter function or directly implement the ``_get_property_list``, ``_get`` and
``_set`` methods of an object (but that goes far beyond the scope of this
tutorial).

Lets add a property that allows us to control the amplitude of our wave.

In our ``gdexample.h`` file we need to add a member variable and getter and setter
functions:

.. code-block:: cpp

    ...
    private:
        double time_passed;
        double amplitude;

    public:
        void set_amplitude(const double p_amplitude);
        double get_amplitude() const;
    ...

In our ``gdexample.cpp`` file we need to make a number of changes, we will only
show the methods we end up changing, don't remove the lines we're omitting:

.. code-block:: cpp

    void GDExample::_bind_methods() {
        ClassDB::bind_method(D_METHOD("get_amplitude"), &GDExample::get_amplitude);
        ClassDB::bind_method(D_METHOD("set_amplitude", "p_amplitude"), &GDExample::set_amplitude);

        ADD_PROPERTY(PropertyInfo(Variant::FLOAT, "amplitude"), "set_amplitude", "get_amplitude");
    }

    GDExample::GDExample() {
        // Initialize any variables here.
        time_passed = 0.0;
        amplitude = 10.0;
    }

    void GDExample::_process(double delta) {
        time_passed += delta;

        Vector2 new_position = Vector2(
            amplitude + (amplitude * sin(time_passed * 2.0)),
            amplitude + (amplitude * cos(time_passed * 1.5))
        );

        set_position(new_position);
    }

    void GDExample::set_amplitude(const double p_amplitude) {
        amplitude = p_amplitude;
    }

    double GDExample::get_amplitude() const {
        return amplitude;
    }

Once you compile the module with these changes in place, you will see that a
property has been added to our interface. You can now change this property and
when you run your project, you will see that our Godot icon travels along a
larger figure.

Let's do the same but for the speed of our animation and use a setter and getter
function. Our ``gdexample.h`` header file again only needs a few more lines of
code:

.. code-block:: cpp

    ...
        double amplitude;
        double speed;
    ...
        void _process(double delta) override;
        void set_speed(const double p_speed);
        double get_speed() const;
    ...

This requires a few more changes to our ``gdexample.cpp`` file, again we're only
showing the methods that have changed so don't remove anything we're omitting:

.. code-block:: cpp

    void GDExample::_bind_methods() {
        ...
        ClassDB::bind_method(D_METHOD("get_speed"), &GDExample::get_speed);
        ClassDB::bind_method(D_METHOD("set_speed", "p_speed"), &GDExample::set_speed);

        ADD_PROPERTY(PropertyInfo(Variant::FLOAT, "speed", PROPERTY_HINT_RANGE, "0,20,0.01"), "set_speed", "get_speed");
    }

    GDExample::GDExample() {
        time_passed = 0.0;
        amplitude = 10.0;
        speed = 1.0;
    }

    void GDExample::_process(double delta) {
        time_passed += speed * delta;

        Vector2 new_position = Vector2(
            amplitude + (amplitude * sin(time_passed * 2.0)),
            amplitude + (amplitude * cos(time_passed * 1.5))
        );

        set_position(new_position);
    }

    ...

    void GDExample::set_speed(const double p_speed) {
        speed = p_speed;
    }

    double GDExample::get_speed() const {
        return speed;
    }

Now when the project is compiled, we'll see another property called speed.
Changing its value will make the animation go faster or slower.
Furthermore, we added a property range which describes in which range the value can be.
The first two arguments are the minimum and maximum value and the third is the step size.

.. note::

    For simplicity, we've only used the hint_range of the property method.
    There are a lot more options to choose from. These can be used to
    further configure how properties are displayed and set on the Godot side.
    You can find more information on property hints here :ref:`@GlobalScope<enum_@GlobalScope_PropertyHint>`.

Signals
-------

Last but not least, signals fully work in GDExtension as well. Having your extension
react to a signal given out by another object requires you to call ``connect``
on that object. We can't think of a good example for our wobbling Godot icon, we
would need to showcase a far more complete example.

This is the required syntax:

.. code-block:: cpp

    some_other_node->connect("the_signal", Callable(this, "my_method"));

To connect our signal ``the_signal`` from some other node with our method
``my_method``, we need to provide the ``connect`` method with the name of the signal
and a ``Callable``. The ``Callable`` holds information about an object on which a method
can be called. In our case, it associates our current object instance ``this`` with the
method ``my_method`` of the object. Then the ``connect`` method will add this to the
observers of ``the_signal``. Whenever ``the_signal`` is now emitted, Godot knows which
method of which object it needs to call.

Note that you can only call ``my_method`` if you've previously registered it in
your ``_bind_methods`` method. Otherwise Godot will not know about the existence
of ``my_method``.

To learn more about ``Callable``, check out the class reference here: :ref:`Callable <class_Callable>`.

Having your object sending out signals is more common. For our wobbling
Godot icon, we'll do something silly just to show how it works. We're going to
emit a signal every time a second has passed and pass the new location along.

In our ``gdexample.h`` header file, we need to define a new member ``time_emit``:

.. code-block:: cpp

    ...
        double time_passed;
        double time_emit;
        double amplitude;
    ...

This time, the changes in ``gdexample.cpp`` are more elaborate. First,
you'll need to set ``time_emit = 0.0;`` in either our ``_init`` method or in our
constructor. We'll look at the other 2 needed changes one by one.

In our ``_bind_methods`` method, we need to declare our signal. This is done
as follows:

.. code-block:: cpp

    void GDExample::_bind_methods() {
        ...
        ADD_PROPERTY(PropertyInfo(Variant::FLOAT, "speed", PROPERTY_HINT_RANGE, "0,20,0.01"), "set_speed", "get_speed");

        ADD_SIGNAL(MethodInfo("position_changed", PropertyInfo(Variant::OBJECT, "node"), PropertyInfo(Variant::VECTOR2, "new_pos")));
    }

Here, our ``ADD_SIGNAL`` macro can be a single call with a ``MethodInfo`` argument.
``MethodInfo``'s first parameter will be the signal's name, and its remaining parameters
are ``PropertyInfo`` types which describe the essentials of each of the method's parameters.
``PropertyInfo`` parameters are defined with the data type of the parameter, and then the name
that the parameter will have by default.

So here, we add a signal, with a ``MethodInfo`` which names the signal "position_changed". The
``PropertyInfo`` parameters describe two essential arguments, one of type ``Object``, the other
of type ``Vector2``, respectively named "node" and "new_pos".

Next, we'll need to change our ``_process`` method:

.. code-block:: cpp

    void GDExample::_process(double delta) {
        time_passed += speed * delta;

        Vector2 new_position = Vector2(
            amplitude + (amplitude * sin(time_passed * 2.0)),
            amplitude + (amplitude * cos(time_passed * 1.5))
        );

        set_position(new_position);

        time_emit += delta;
        if (time_emit > 1.0) {
            emit_signal("position_changed", this, new_position);

            time_emit = 0.0;
        }
    }

After a second has passed, we emit our signal and reset our counter. We can add
our parameter values directly to ``emit_signal``.

Once the GDExtension library is compiled, we can go into Godot and select our sprite
node. In the **Node** dock, we can find our new signal and link it up by pressing
the **Connect** button or double-clicking the signal. We've added a script on
our main node and implemented our signal like this:

.. code-block:: gdscript

    extends Node

    func _on_Sprite2D_position_changed(node, new_pos):
        print("The position of " + node.get_class() + " is now " + str(new_pos))

Every second, we output our position to the console.

Next steps
----------

We hope the above example showed you the basics. You can build upon this example to create full-fledged scripts
to control nodes in Godot using C++!

Create further extensions from EGP's C++ panel to keep the native build layout
and SDK compatibility checks consistent. Extend this example with your own
nodes, resources and signals, then qualify each target platform independently.
