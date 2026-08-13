# Adrien Perello-y-Bestard — academic website

Source for [adrien-perello.github.io](https://adrien-perello.github.io/), a minimal public interface to Adrien's research, publications and selected projects.

## Architecture

The site uses Hugo without a theme or Hugo Modules. The previous Hugo Blox academic demo was removed because its block system, sample content and dependency graph added maintenance burden without helping the new design. Hugo remains as a small static generator because it provides reliable Markdown content, clean URLs and fast GitHub Pages builds without client-side JavaScript.

The rendered site has no analytics, trackers, external fonts or runtime JavaScript. Light and dark palettes follow the visitor's operating-system preference.

## Local development

Install Hugo `0.165.0`, then run:

```sh
hugo server -D
```

Open `http://localhost:1313/`.

## Production build and checks

```sh
hugo --gc --minify
python3 scripts/check_site.py public
```

The checker verifies generated pages, essential metadata, heading structure, image alternatives and internal links.

## Content map

- `content/` — Home, Research, Publications & Outputs, Projects and About copy.
- `data/publications.yaml` — version-controlled publication, dataset and report metadata.
- `data/projects.yaml` — evidence-backed project records.
- `layouts/` — semantic page templates and metadata.
- `assets/css/main.css` — the complete design system.
- `assets/images/` — source images processed into responsive formats by Hugo.
- `archetypes/artifacts.md` — private-first scaffold for later evidence-bearing artifacts.
- `docs/content-maintenance.md` — publication and evidence-status rules.

Research Notes and Artifacts are deliberately not visible until mature public material exists.

## Deployment

`.github/workflows/publish.yaml` builds `main` with the pinned Hugo version, validates `public/`, uploads the static artifact and deploys it through GitHub Pages. No generated site files are committed.

## Updating scholarly records

Publication and output metadata must be verified against a DOI/publisher or repository record before editing `data/publications.yaml`. Profiles such as Google Scholar and ORCID are links and discovery aids, not runtime data sources.

See [docs/content-maintenance.md](docs/content-maintenance.md) for status definitions and future artifact rules.
