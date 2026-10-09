.. _doc_egp_reference_workflow:

Maintaining the published reference
===================================

Use a clean engine checkout at the source commit you intend to document.
From the documentation repository:

.. code-block:: console

   python tools/sync_egp_docs.py --engine ../EGP-Engine
   python tools/sync_egp_docs.py --engine ../EGP-Engine --check
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

Synchronizing official upstream changes
-------------------------------------------

Keep the official repositories as ``upstream`` remotes in each fork. In a clean
checkout, fetch the branch before comparing it with the published EGP history:

.. code-block:: console

   git fetch upstream master
   git merge-base HEAD upstream/master
   git rev-list --left-right --count upstream/master...HEAD
   git log HEAD..upstream/master --oneline

The left count is upstream commits missing from the fork; the right count is
fork commits missing from upstream. A shallow boundary can hide the shared
history and inflate those counts. Deepen the relevant upstream history until
the common base and incoming commit list can be verified.

Review incoming changes in an isolated checkout before merging. Preserve EGP's
intentional networking/physics replacements, generated class reference,
deployment configuration and attribution. Regenerate classes from the qualified
EGP engine revision; importing vanilla Godot class pages would restore APIs that
EGP removes. Review upstream tutorial changes against those same contracts.

The engine integration owner verifies source compatibility, builds, SDK/bindings
and runtime regressions before publishing a new canonical revision. Then update
this manual from that exact revision, run freshness and Sphinx checks, and build
the website with its link/asset checks. Record the upstream tips, merge commit,
qualified source and test results together. A successful fetch alone does not
establish that source is merged or compatible; publishing documentation does not
establish runtime compatibility.
