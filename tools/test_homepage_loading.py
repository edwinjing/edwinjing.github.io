"""Guard production font, image and deferred-media loading without network."""
from html.parser import HTMLParser
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
site = root / 'site'
html = (site / 'index.html').read_text()
css = (site / 'stylesheets/edwinos.css').read_text()
assert not re.search(r'fonts\.(?:googleapis|gstatic)\.com', html + css)
fonts = re.findall(r'@font-face\s*\{(.*?)\}', css, re.S)
assert fonts and all('font-display: swap' in block for block in fonts)
for block in fonts:
    for url in re.findall(r'url\([\'"]?([^\)\'\"]+)', block):
        assert url.startswith('../assets/fonts/') and (site / 'stylesheets' / url).is_file(), url

class Tags(HTMLParser):
    def __init__(self):
        super().__init__(); self.images = []; self.links = []; self.media = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'img': self.images.append(a)
        if tag == 'link': self.links.append(a)
        if tag in ('video', 'iframe'): self.media.append(a)
tags=Tags();tags.feed(html)
assert tags.images, 'Lightbox/parser removed all images'
avatar=next(a for a in tags.images if 'avatar-edwin' in a.get('src',''))
assert avatar.get('loading') == 'eager' and avatar.get('fetchpriority') == 'high'
assert any(a.get('loading')=='lazy' for a in tags.images)
assert any(a.get('srcset') and a.get('sizes') and a.get('width') and a.get('height') for a in tags.images)
assert any(a.get('rel')=='preload' and a.get('as')=='image' for a in tags.links)
assert any(a.get('rel')=='preload' and a.get('as')=='font' for a in tags.links)
assert all(not a.get('src') for a in tags.media), 'PDF/video must wait for reader intent'
assert 'data-progressive-image' in html
print('PASS: same-origin swap fonts, first-screen priority, responsive/lazy images and deferred media')
