# Homepage deployment

This repository deploys **https://edwinjing.github.io/**. Its checkout is normally
`/Users/edwin/Documents/homepage`; never run these publishing commands in the old
blog checkout. The existing `edwinjing-blog.com` repository is independent.

## Release contract

`.github/workflows/deploy.yml` is the authoritative pipeline. Pushes to `main`
or a manual workflow dispatch install the tested Python 3.12 environment, verify
image-parser compatibility, build with MkDocs `--clean --strict`, check content,
SEO and asset/loading contracts, and upload/deploy `site/` through GitHub Pages.
Repository **Settings → Pages → Source** must be **GitHub Actions**. HTTPS remains
required; no CNAME is used for this organization homepage.

```sh
.venv/bin/python -m pip install -r requirements.lock.txt
.venv/bin/mkdocs build --clean --strict
.venv/bin/python tools/test_homepage_build.py
.venv/bin/python tools/test_homepage_loading.py
.venv/bin/python -m unittest discover -s tools -p test_glightbox_compatibility.py
git diff --check
# Review and stage only intended files, commit, then:
git push origin main
```

Publishing requires Edwin's request. This first publication was explicitly
authorized on 2026-10-27. Do not infer later publication permission from local UI
work alone. After each push, inspect the matching commit's **Deploy MkDocs to
GitHub Pages** run, then verify the real website. A green run alone is insufficient.

## Loading contract to preserve

- `theme.font: false`; all font faces use same-origin WOFF2 with `font-display: swap`.
  No Google Fonts imports or preconnects. Critical font preloads remain local.
- Keep avatar priority and existing first-image preloads. Do not make every image
  lazy: above-the-fold images should not wait for a scroll.
- Preserve responsive local thumbnails, intrinsic aspect ratios, blur previews
  and decode readiness. Below-fold/later images retain native lazy loading.
- PDF/video resources load only after reader intent. Do not preload media clips.
- Python 3.12, `mkdocs-glightbox==0.5.2`, `selectolax==0.4.10` are tested together.
  Update the lockfile deliberately; verify actual generated `<img>` nodes.
- No homepage search corpus or Google Fonts network requests.
- The visitor badge keeps the shared blog key. Latest updated queries the latest
  successful push run of **this repository's `deploy.yml`**, with authored fallback
  if the public GitHub API is temporarily unavailable/rate-limited.

## Production acceptance

Check desktop and narrow layouts, light/dark themes, chapter navigation (no orange
highlight), menu, profile/avatar and all visible images. Inspect browser network
resources: font URLs must be same-origin and critical images must have positive
natural dimensions. Confirm canonical/robots/sitemap use the new domain, blog
entry links still lead to the old blog, and homepage opening makes no PDF/video
requests. Network timings are environment-dependent; record conditions, not a
universal loading-speed guarantee.
