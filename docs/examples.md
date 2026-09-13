# Examples

The `examples/` directory contains small, executable consumers of the public registry.

## Current examples

### Python discovery

`examples/python_discovery.py` demonstrates loading repository records locally and performing a basic discovery workflow.

### jq queries

`examples/query_with_jq.sh` demonstrates filtering the canonical JSON dataset with `jq`.

## Example standard

New examples should answer a real downstream question and document:

- purpose;
- source file or partition;
- expected input;
- execution command;
- expected output shape;
- snapshot assumptions;
- limitations.

Examples should not modify canonical dataset files.

## Useful future examples

- language distribution report;
- topic exploration;
- metadata completeness report;
- local repository index;
- reproducible ecosystem analysis;
- retrieval/RAG preparation.

Future examples should be added only when they are tested against the actual repository structure and fields.
