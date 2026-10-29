"""Check site assets and navigation without third-party dependencies."""
from html.parser import HTMLParser
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent

class SiteParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.refs, self.images = [], [], []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        for key in ('src', 'href', 'poster', 'data-still', 'data-animation'):
            if key in attrs:
                self.refs.append(attrs[key])
        if tag == 'img':
            self.images.append(attrs)
        if tag == 'a' and attrs.get('target') == '_blank':
            assert 'noopener' in attrs.get('rel', ''), 'External tab needs noopener'

site = SiteParser()
site.feed((ROOT / 'index.html').read_text())
assert len(site.ids) == len(set(site.ids)), 'Duplicate element IDs'
for ref in site.refs:
    if ref.startswith('#'):
        assert ref[1:] in site.ids, f'Missing anchor {ref}'
    elif not re.match(r'^[a-z]+:', ref):
        assert (ROOT / ref).is_file(), f'Missing asset: {ref}'
for image in site.images:
    assert image.get('alt'), 'Image needs meaningful alt text'
    assert image.get('width') and image.get('height'), 'Image needs dimensions'
for font in ('jetbrains-mono',):
    assert (ROOT / f'assets/fonts/{font}.woff2').stat().st_size > 1000
for gif in ('mule', 'llm', 'diffusion'):
    assert (ROOT / f'assets/{gif}.gif').read_bytes()[:6] in (b'GIF87a', b'GIF89a')
    assert (ROOT / f'assets/color/{gif}.gif').read_bytes()[:6] in (b'GIF87a', b'GIF89a')
    assert (ROOT / f'assets/color/{gif}-still.png').read_bytes()[:8] == b'\x89PNG\r\n\x1a\n'
assert not list((ROOT / 'assets').rglob('*.pdf')), 'Private CV must stay outside public assets'
print(f'Passed: {len(site.refs)} asset/link references, {len(site.ids)} unique IDs, 3 GIFs, fonts, and private-CV exclusion.')
