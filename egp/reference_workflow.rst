.. _doc_egp_reference_workflow:

Maintaining the published reference
===================================

Use a clean engine checkout at the source commit you intend to document.
From the documentation repository:

.. code-block:: console

   python tools/sync_egp_docs.py --engine ../EGP
   python tools/sync_egp_docs.py --engine ../EGP --check
   python -m sphinx -b html -W --keep-going -j 4 . _build/html

This wrapper first invokes the engine's class/manual generator, then renders
public C# and C++ helper declarations from the same source revision. It retains
multiline signatures, overloads, default arguments, events and property
accessors, while excluding method bodies and private implementation fields.
GDScript declarations and signals come from the engine generator.

``egp/source_manifest.json`` records the pinned engine revision, normalized
source hashes, output hashes and the documentation generator hash. CI checks
the complete generated result against that engine commit before building.
Update source helpers and their behavior documentation in the engine first;
update additional tutorials and language examples in this repository.

The engine's ``misc/scripts/sync_egp_docs.py`` remains the base generator.
When updating this documentation fork, run the wrapper above so that the typed
helper reference and its manifest are completed together.

The manual synchronization workflow exports a reviewable patch. Commit the
result only after reviewing the source revision, API changes and relevant
qualification record. The Pages workflow publishes a build with Sphinx
warnings treated as errors.
