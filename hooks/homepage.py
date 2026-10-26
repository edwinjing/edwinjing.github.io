"""Independent homepage build contract; the original blog remains untouched."""
from __future__ import annotations

import re
from html.parser import HTMLParser
from pathlib import Path

from mkdocs.exceptions import PluginError


class FriendCards(HTMLParser):
    """Match the source blog runtime's real-card counting rule."""

    def __init__(self):
        super().__init__()
        self.count = 0

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if "friend-card" not in attrs.get("class", "").split() or "href" not in attrs:
            return
        if not re.match(r"https?://example\d*\.com/?", attrs["href"] or "", re.I):
            self.count += 1


def on_page_markdown(markdown, page, config, files):
    if page.file.src_uri != "index.md":
        raise PluginError("The independent homepage must only publish index.md")
    source = Path(config.config_file_path).parent / "data/homepage/friends-source.md"
    if not source.is_file():
        raise PluginError("Missing homepage Friends count source: " + str(source))
    parser = FriendCards()
    parser.feed(source.read_text(encoding="utf-8"))
    marker = r'(<span\b[^>]*\bid="friend-count"[^>]*>)[^<]*(</span>)'
    result, replacements = re.subn(marker, lambda match: f"{match[1]}{parser.count}{match[2]}", markdown)
    if replacements != 1 or 'data-friend-count-static="true"' not in result:
        raise PluginError("Expected exactly one static homepage Friends count")
    return result


def on_files(files, config):
    # Preserve shared visual code, but do not publish the retired search bootstrap.
    for item in list(files):
        if item.src_uri == "javascripts/search-loader.js":
            files.remove(item)
    return files
