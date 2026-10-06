.. _doc_egp_hot_reload:

Runtime hot reload
==================

EGP supports opted-in C# and C++ reload in games launched by an editor build.
Set ``debug/hot_reload/enable_runtime=true`` before launching the game.
Export templates keep runtime reload disabled. C# uses collectible assemblies
when enabled; libraries that require non-collectible assemblies should retain
the default setting.

Building and reloading
----------------------

The C++ extension panel publishes successful Debug builds and notifies
attached games. C# Build sends the same debugger command. The game processes
native reload at an idle boundary before refreshing script bindings.
Failed compilation retains the previously published native descriptor/library.
Stop the game before Release extension builds.

Compatible changes can preserve native object identity, saved properties,
callables and subscriptions. Application threads must shut down through the
application's own lifecycle. Static state, arbitrary layouts and inheritance
changes require deliberate migration and validation.

Recovery and restart
--------------------

Missing or invalid libraries keep native parents and saved extension state
available for compatible repair. Changing a class's native base or removing
a live class requires repair or restart. Changing a method signature invalidates
cached native bindings; update callers. Dynamic lookup uses the repaired API,
while code holding raw cached bindings may need a restart.

Corrupted managed assemblies and blocked unloads have separate recovery paths.
Do not treat a successful single reload as long-session memory qualification.
See :doc:`cpp_extensions` and :doc:`api_contract` for the detailed contract and
the targeted ``validate_egp_hot_reload.py`` flags.
