# Contributing

Contributions are welcome when they improve correctness, reproducibility, security, documentation, or maintainability.

## Development

1. Fork or clone the repository.
2. Create a focused branch.
3. Install dependencies from `requirements.txt`.
4. Run `python -m unittest discover -s tests -v`.
5. Keep data-model changes synchronized with `schema/repository.schema.json` and documentation.
6. Do not commit GitHub tokens or other secrets.

## Data changes

Do not manually edit generated files under `data/` or repository entries in `README.md`. Generated data is produced by `generate_list.py`.

Changes to inclusion rules or derived classifications must be explicit, documented, and covered by tests.

## Pull requests

Keep pull requests narrowly scoped. Explain behavior changes, tests performed, and any changes to the public data contract.
