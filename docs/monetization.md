# Sustainable monetization model

RepoSource Registry should monetize services around the open dataset, not degrade the public dataset to force payment.

| Model | Customer | Value | Priority | Open-source boundary |
|---|---|---|---|---|
| GitHub Sponsors | Users and maintainers | Direct support for maintenance | Immediate | Public dataset remains open |
| Company sponsorship | Developer/data companies | Fund ecosystem infrastructure | After adoption evidence | No ranking or data influence |
| Support/consulting | Teams using the registry | Integration and implementation help | Opportunistic | Core project remains public |
| Custom datasets | Companies/researchers | Tailored derived views | Validate demand first | Generic methodology stays public |
| API subscription | High-volume applications | Convenience, scale, reliability | Later | Static public dataset remains useful |
| Historical snapshots | Researchers and data teams | Longitudinal analysis | Later | Public snapshots can remain available where practical |
| Analytics | Ecosystem teams | Trends, comparisons, alerts | Later | Raw public foundation remains open |
| Enterprise exports | Larger organizations | Operational integration | Later | No private manipulation of public rankings |

## Product ladder

**Open layer:** canonical JSON/CSV, schema, indexes, methodology, examples, provenance.

**Developer layer:** CLI, SDK, static query helpers, and eventually a free API if demand justifies them.

**Intelligence layer:** history, trends, similarity, recommendations, alerts, and ecosystem analytics.

**Commercial layer:** higher-volume API access, enterprise exports, managed integrations, and custom analytics.

## Decision rule

Do not build a paid service because it sounds monetizable. Build it when repeated users encounter a measurable limitation in the free static dataset and at least one customer is willing to pay to remove that limitation.

## Trust guardrails

- The canonical public dataset remains accessible.
- Provenance and methodology remain transparent.
- Paid services add convenience, scale, historical depth, or analysis.
- Sponsor identity cannot alter ranking or classification rules.
- No private user information is sold.
- No deceptive claims or fabricated adoption metrics.
