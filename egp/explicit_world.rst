.. _doc_egp_explicit_world:


Explicit physics worlds
=======================

``EGPBox3DWorld`` provides independent fixed ticks, stable body IDs, ordered
commands and trusted local snapshots. It does not automatically restore
SceneTree physics bodies.

Superpos requires a separately qualified native simulation provider to attach
physics. The retired networking physics helper is unavailable. See :doc:`box3d`
and :doc:`networking_reference`.
