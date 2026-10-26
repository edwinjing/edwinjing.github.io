"""Check the rendered migration boundaries without network or source mutations.

Usage: .venv/bin/python tools/test_homepage_build.py [site-directory]
"""
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit


class Document(HTMLParser):
    def __init__(self):
        super().__init__()
        self.nodes = []

    def handle_starttag(self, tag, attributes):
        self.nodes.append((tag, dict(attributes)))


root = Path(__file__).resolve().parents[1]
site = (root / (sys.argv[1] if len(sys.argv) > 1 else "site")).resolve()
html = (site / "index.html").read_text()
doc = Document()
doc.feed(html)
ids = [attrs["id"] for tag, attrs in doc.nodes if "id" in attrs]
for identifier in ("about", "news", "education", "experience", "publications", "workshops", "honors"):
    assert ids.count(identifier) == 1, f"Missing/duplicate chapter: {identifier}"
assert html.index('id="about"') < html.index('class="academic-sidebar"'), "About must precede mobile profile"
anchors = {attrs.get("href") for tag, attrs in doc.nodes if tag == "a"}
for target in ("HOME/Archive/", "HOME/friends/", "OsdNotes/", "经验分享/"):
    assert "https://edwinjing-blog.com/" + target in anchors, f"Missing blog outbound link {target}"
assert 'data-friend-count-static="true">2</span>' in html, "Baseline Friends count changed"
assert 'data-deployment-repository="edwinjing/edwinjing.github.io"' in html
assert "path=https%3A%2F%2Fedwinjing-blog.com%2F" in html, "Shared visitor key changed"
canonical = [attrs["href"] for tag, attrs in doc.nodes if tag == "link" and attrs.get("rel") == "canonical"]
assert canonical == ["https://edwinjing.github.io/"], canonical
assert not re.search(r'<meta[^>]+content="[^"]*(?:noindex|nosnippet)', html, re.I)
assert 'name="description"' in html
for schema in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
    graph = json.loads(schema)["@graph"]
    assert all(item["@id"].startswith("https://edwinjing.github.io/") for item in graph)
assert "https://edwinjing.github.io/sitemap.xml" in (site / "robots.txt").read_text()
assert "https://edwinjing-blog.com/" not in (site / "sitemap.xml").read_text()
for path in ("CNAME", "BingSiteAuth.xml", "HOME", "OsdNotes", "经验分享", "blog", "research", "search", "javascripts/search-loader.js"):
    assert not (site / path).exists(), f"Unexpected published blog/search content: {path}"
assert "search-loader.js" not in html and "search-exact-worker" not in html
for tag, attrs in doc.nodes:
    urls = []
    if tag in ("img", "script", "source") and attrs.get("src"):
        urls.append(attrs["src"])
    if attrs.get("srcset") and not attrs["srcset"].startswith("data:"):
        urls.extend(entry.strip().split()[0] for entry in attrs["srcset"].split(","))
    if tag == "link" and attrs.get("href"):
        urls.append(attrs["href"])
    if tag == "a" and attrs.get("href", "").startswith("assets/"):
        urls.append(attrs["href"])
    for url in urls:
        parsed = urlsplit(url)
        if parsed.scheme or parsed.netloc or not parsed.path:
            continue
        asset = site / unquote(parsed.path).lstrip("/")
        assert asset.exists(), f"Missing local resource: {url}"
print("PASS: homepage content, section targets, outbound links, SEO, shared footer, assets and publication scope")
