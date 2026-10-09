.. _doc_egp_prediction:


Native prediction
=================

Superpos prediction requires a registered, compiled native simulation provider
and explicit history/byte bounds. Script callbacks do not register a qualified
provider. Unregistered sessions fail closed. The current replay fixture does
not establish a Box2D/Box3D solver adapter or cross-platform recovery.

See :doc:`networking_reference` and :doc:`box3d`.
