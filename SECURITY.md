# Security Policy

## Scope

Security issues in the RepoSource Registry code, GitHub Actions workflows, dependency configuration, data-generation pipeline, and generated data handling are in scope.

## Reporting

Please do not disclose exploitable vulnerabilities in public issues. Report security issues privately through the repository owner's available GitHub security reporting mechanism.

When reporting, include:

- affected file or workflow
- reproducible steps
- security impact
- suggested mitigation, if known

## Security principles

- GitHub metadata is treated as untrusted input.
- Credentials must come from environment variables or GitHub Actions secrets.
- Workflow permissions follow least privilege.
- Generated Markdown and CSV are handled defensively.
- Tests should cover security-sensitive parsing and generation behavior.
