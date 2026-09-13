# Growth strategy

The growth model is a product flywheel, not a traffic campaign.

## Flywheel

Useful dataset → developer discovers it → developer uses it → developer cites or stars it → issues and contributions improve it → the dataset becomes more reliable → more tools and researchers use it → companies recognize recurring infrastructure value → sponsorship and commercial extensions become possible.

## Acquisition channels

### GitHub

Improve the repository description, relevant topics, README clarity, examples, releases, contribution experience, and issue quality. Do not manufacture engagement.

### Search

Publish useful, non-duplicative documentation around the real concepts represented by the dataset: GitHub repository dataset, repository discovery, repository metadata, programming-language repositories, open-source project discovery, and machine-readable GitHub data.

### AI and developer tools

Keep `dataset.json`, `llms.txt`, the JSON Schema, data dictionary, methodology, and canonical data paths explicit. Encourage users to verify important facts against the upstream GitHub repository.

### Community

Invite data-quality reports, use-case examples, integrations, and research applications. A contributor should be able to understand the architecture and run the tests without private context.

## Metrics that matter

Prioritize:

- unique downstream users or projects that actually consume the data;
- forks and meaningful contributions;
- external citations and references;
- repeat dataset downloads or API usage once measurable infrastructure exists;
- issue reports that improve correctness;
- sponsorship from users or companies with a demonstrated reason to depend on the project.

Stars are useful as a discovery signal but are not the product goal.

## Anti-patterns

Do not buy stars, create fake issues, manufacture testimonials, mass-post links, keyword-stuff documentation, scrape personal contact data, or create artificial contributor activity.

## Validation loop

Every proposed growth feature should answer: who needs this, what evidence shows they need it, how will we measure usefulness, and what maintenance cost does it introduce?
