# Contributing

Start with an item in [the backlog](docs/backlog.md). The first milestone is a serial, observable budget loop, not a general multi-agent platform.

Use Python 3.11+, install `requirements-dev.txt`, and run `python scripts/check_protocol.py`. Do not execute commands copied from a plan merely to validate the protocol.

For behavior changes, explain the user-visible problem, the change, and the evidence that verifies it. Add focused regression checks for budgeting, recovery, scope enforcement, and acceptance behavior. For adapters, provide redacted output fixtures and distinguish measured values from estimates and unknowns.

Do not commit credentials, account identifiers, local transcripts, task repositories, or private source code. Receipts used in research must be redacted and carry model/configuration versions and accounting confidence.

Do not claim quota savings from schema validation or mocked runs. Protocol changes must update the examples, documentation, and versioning decision together. Draft 0.2 is not a stable public interface.

Contributions are provided under the project's MIT license.
