# Vercel public discovery

RepoSource Registry can be deployed to Vercel as a lightweight public discovery interface around the existing open dataset.

## Architecture

The GitHub repository remains the source project and canonical data distribution. The Vercel application is a presentation/discovery layer. It does not create a separate database and it does not replace the collection pipeline.

The current implementation uses Next.js App Router and server-rendered pages. Repository search and detail pages read the canonical `data/repositories.json` snapshot from the public GitHub raw distribution with a one-hour revalidation window. Dataset statistics are read from `data/statistics.json` using the same cache policy.

This deliberately avoids copying the 40 MB canonical registry into a second frontend artifact. It also avoids a database and avoids a paid or metered data-access product.

## Routes

- `/` — product overview, current statistics, language/category exploration, and trust model.
- `/search` — server-rendered search, language/category filters, minimum-star filter, and result links.
- `/repo/[owner]/[name]` — snapshot detail view for an individual repository.
- `/data` — canonical dataset, schema, manifest, statistics, methodology, and agent resources.
- `/robots.txt` — generated crawler rules.
- `/sitemap.xml` — generated for the public web origin when `SITE_URL` or Vercel's deployment URL is available.

Repository detail pages are generated on demand rather than pre-generating thousands of thin pages.

## Local development

Requirements: Node.js compatible with the selected Next.js release.

```bash
npm install
npm run dev
```

Open the local development URL shown by Next.js.

## Production build

```bash
npm run build
npm start
```

The build does not regenerate the RepoSource dataset and does not invoke GitHub Search.

## Vercel deployment

The repository is structured for Vercel's automatic Next.js detection. The simplest deployment path is to import `SamoTech/RepoSource-Registry` into Vercel and use the repository's `main` branch.

No environment variables are required for the core application. `SITE_URL` is optional and can be set to the final public origin when a custom domain is configured. If it is not set, Vercel's `VERCEL_URL` is used for generated sitemap output.

The project does not contain deployment credentials or tokens.

## Caching and dataset loading

The canonical dataset is approximately 40 MB in the current manifest. The frontend therefore does not ship the entire registry to every browser. Server-rendered discovery requests fetch the canonical snapshot and use Next.js/Vercel revalidation caching.

This is intentionally a simple first deployment. If real usage demonstrates a performance problem, the next step should be a generated compact discovery index or additional static partitions—not a database introduced by default.

## Security

Repository metadata is treated as untrusted input and rendered through React escaping. Upstream repository URLs are used as links rather than injected HTML. No credentials are required by the frontend. The application contains no authentication or user-submitted HTML surface.

## Limitations

- Search is limited to the published snapshot and is not live GitHub Search.
- The canonical dataset is large, so the first uncached server request can be materially more expensive than a small static page.
- Search results are capped at 100.
- Snapshot values such as stars, descriptions, and topics can change upstream.
- The website is not the authoritative source for current repository facts.

## Future improvements

Only if actual usage justifies them:

- compact generated search indexes;
- static popular-repository views;
- language/topic browsing pages with meaningful content;
- performance measurement with privacy-respecting telemetry;
- richer visualization and research workflows.

The public dataset remains directly accessible regardless of whether these features are implemented.
