"""Limit academic pages and derive their profile count from the Friends page."""
from __future__ import annotations

import re
from html.parser import HTMLParser
from pathlib import Path

from mkdocs.exceptions import PluginError
from mkdocs.plugins import event_priority


FRIENDS_PAGE = "HOME/friends.md"


class FriendCards(HTMLParser):
    """Count authored friend links while skipping examples."""

    def __init__(self):
        super().__init__()
        self.count = 0

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if "friend-card" not in attrs.get("class", "").split() or "href" not in attrs:
            return
        if not re.match(r"https?://example\d*\.com/?", attrs["href"] or "", re.I):
            self.count += 1


@event_priority(-10)
def on_page_content(html, page, config, files):
    # Run after home_sections has inserted the shared profile on Friends.
    if page.file.src_uri not in ("index.md", FRIENDS_PAGE):
        raise PluginError("The academic site can only publish Overview and Friends")
    source = Path(config["docs_dir"]) / FRIENDS_PAGE
    try:
        friends = source.read_text(encoding="utf-8")
    except OSError as exc:
        raise PluginError(f"Missing Friends count source: {source}") from exc
    parser = FriendCards()
    parser.feed(friends)
    marker = r'(<span\b[^>]*\bid="friend-count"[^>]*>)[^<]*(</span>)'
    result, replacements = re.subn(marker, lambda match: f"{match[1]}{parser.count}{match[2]}", html)
    if replacements != 1 or 'data-friend-count-static="true"' not in result:
        raise PluginError("Expected exactly one static homepage Friends count")
    return result


def on_files(files, config):
    # Preserve shared visual code, but do not publish the retired search bootstrap.
    for item in list(files):
        if item.src_uri == "javascripts/search-loader.js":
            files.remove(item)
    return files
