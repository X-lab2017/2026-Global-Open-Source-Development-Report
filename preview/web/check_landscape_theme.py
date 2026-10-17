"""Protect the accepted brand and readable text when 4.1 is viewed in either theme."""
import argparse
import re
from pathlib import Path
import goso_brand as B

parser = argparse.ArgumentParser()
parser.add_argument('--output', type=Path, required=True)
args = parser.parse_args()
css = (args.output / 'landscape-theme.css').read_text()
page = (args.output / '2026/zh/chapters/04/index.html').read_text()

def luminance(value):
    channels = [int(value[i:i+2], 16) / 255 for i in (1, 3, 5)]
    rgb = [x / 12.92 if x <= .04045 else ((x + .055) / 1.055) ** 2.4 for x in channels]
    return sum(x * w for x, w in zip(rgb, [.2126, .7152, .0722]))

def contrast(a, b):
    values = sorted([luminance(a), luminance(b)])
    return (values[1] + .05) / (values[0] + .05)

for theme in ['light', 'dark']:
    prefix = '' if theme == 'light' else '[data-theme="dark"] '
    selector = ','.join(prefix + s for s in ['.al-chapter', '#al-fullscreen', '#al-project-dialog'])
    block = css.split(selector + '{', 1)[1].split('}', 1)[0]
    tokens = dict(re.findall(r'(--[\w-]+):(#[0-9A-Fa-f]{6});', block))
    for key, value in B.values(theme).items():
        if value.startswith('#'):
            assert tokens['--gv-' + key].lower() == value.lower(), (theme, key)
    for surface in ['--gv-surface', '--gv-raised']:
        for ink in ['--gv-ink', '--gv-muted', '--gv-brand', '--gv-gold']:
            assert contrast(tokens[ink], tokens[surface]) >= 4.5, (theme, ink, surface)
    for layer in ['agent', 'model']:
        assert contrast(tokens['--al-' + layer], tokens['--al-' + layer + '-soft']) >= 4.5
    assert contrast(tokens['--gv-button'], tokens['--gv-buttonText']) >= 4.5
assert 'data-design-version="4.1-polish-v1"' in page
assert 'landscape-theme.css?v=4.1-polish-v1' in page
assert page.count('data-al-theme') == 2
assert page.count('class="al-panel al-atlas-panel"') == 2
assert 'class="atlas-panel' not in page
assert 'class="atlas-period' not in page
print('PASS 4.1 theme: pinned brand tokens, accessible primary text in both themes, dialog token scopes, isolated atlas classes and reading/fullscreen theme controls.')
