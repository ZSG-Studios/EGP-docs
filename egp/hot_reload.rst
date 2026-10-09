.. _doc_egp_hot_reload:


.. _doc_egp_cpp_owner_handoff:


Runtime reload
==============

Opt in to editor-run runtime reload with
``debug/hot_reload/enable_runtime=true``. Export templates disable it.
Compatible state and bindings require the same editor API; ABI/base changes
can require restart. Applications own their thread/static-state lifecycle.

Superpos has native owner retirement and managed reload hooks. Old transport
owner-handoff and reload fixtures do not qualify Superpos. Current full-engine
reload, generated SDKs and application behavior require separate evidence.
See :doc:`api_contract`, :doc:`cpp_extensions` and :doc:`qualification`.
