# Content maintenance

The public site follows an evidence-status discipline. Add content only when it is accurate, useful to an external reader and safe to disclose.

## Controlled statuses

- **Peer reviewed**: published scholarly output.
- **Preprint / accepted / submitted**: use the exact current status.
- **Benchmark release**: frozen, versioned evaluation artifact with a protocol and limitations.
- **Research prototype**: implemented research artifact, not a validated product.
- **Exploratory**: unresolved research object whose early disclosure is useful.
- **Archived / prior work**: evidence of trajectory that is no longer central to the programme.

Do not use presentation quality to imply stronger evidence. Record limitations, version identifiers and negative or null results when scientifically material.

## Add a publication or output

Edit `data/publications.yaml`. Keep DOI and repository metadata version controlled; the site does not scrape Google Scholar or ORCID. Put peer-reviewed articles under `peer_reviewed` and datasets or reports under `outputs`.

## Add a project

Edit `data/projects.yaml`. A project needs a factual status, a bounded description, Adrien's verified contribution and at least one public evidence link.

## Add a future artifact

Use `hugo new artifacts/<slug>.md`. Keep the draft private until the relevant evidence and disclosure gate is passed. A public artifact should state its purpose, evidence, version, reusable files, limitations and citation information.

Research notes and artifacts remain absent from navigation until substantive public content exists.

## Release check

Run:

```sh
hugo --gc --minify
python3 scripts/check_site.py public
rg -n -i "GenCoin|University X|Hugo Blox|Wowchemy|Lorem ipsum|MIT|test@example|GeorgeCushen|example project" --glob '!public/**'
```

