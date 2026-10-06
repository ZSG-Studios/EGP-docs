.. _doc_webrtc:

WebRTC migration
================

The WebRTC peer and multiplayer classes are not part of EGP's supported
networking API. EGP uses a native desktop Yojimbo transport with encrypted
admission, authoritative entities and explicit message registration.

See :doc:`/egp/networking` for the replacement workflow and
:doc:`/egp/migration` for the API mapping. Browser multiplayer is not established
by the desktop transport; do not adapt upstream WebRTC samples as though they
were EGP client/server examples.
