.. _doc_egp_admission_testing:


Authenticated transport checks
==============================

A configured canonical world alone is not network admission. Provision a native
association through ``configure_udp()`` and check ``get_admission_state()``.
Never log admission keys. The old token protocol and fixtures are retired.

The current engine's ``validate_superpos.py`` tests authenticated separate-process
loopback delivery; WAN, account services and gameplay require separate checks.
See :doc:`network_lab` and :doc:`networking_reference`.
