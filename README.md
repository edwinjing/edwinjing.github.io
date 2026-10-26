# Chen Jing · Academic homepage

Independent MkDocs + Material / EdwinOS copy of the full Overview, intended for
https://edwinjing.github.io/. Published through GitHub Actions; see DEPLOYMENT.md for the release contract.

## Local development

Use Python 3.12 and a project-local environment:

```sh
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements.lock.txt
.venv/bin/mkdocs build --strict
.venv/bin/mkdocs serve --dev-addr 127.0.0.1:8000
```

The current `.venv` is already installed. Preview: http://127.0.0.1:8000/.
`requirements.lock.txt` freezes the tested environment, including the
selectolax compatibility pin needed by the image lightbox.

## Ownership

- `docs/index.md`: unchanged Overview body, section IDs, outbound blog links.
- `data/homepage/`: News, publications and frozen Friends source.
- `hooks/home_sections.py`, `hooks/homepage.py`: homepage build preparation.
- `overrides/partials/header.html`: academic navigation and native theme toggle.
- `docs/stylesheets/edwinos.css`: the single EdwinOS custom stylesheet.
- `docs/javascripts/ui-perf.js`: existing runtime and academic header interactions.
- `implementation/`: baseline, review evidence and implementation decisions.
- `STATE.md`, `TODO.md`: current progress and next review steps.

The original blog at `/Users/edwin/Documents/edwinjing-blog-website` is a read-only
source, not this project's build/deployment target. This repository has its own
Git history and origin. The initial publication was authorized on 2026-10-27. The independent
`.github/workflows/deploy.yml` publishes pushes to `main`; do not copy the blog's
CNAME or change its Pages configuration. See `DEPLOYMENT.md` for checks and updates.
