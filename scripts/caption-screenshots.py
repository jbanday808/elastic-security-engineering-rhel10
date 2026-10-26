#!/usr/bin/env python3
"""Append lossless caption panels. Requires Python 3 and Pillow; uses DejaVu Sans."""
from pathlib import Path
import hashlib
import json
import re
from PIL import Image, ImageDraw, ImageFont, PngImagePlugin

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'assets/screenshots'
OUTPUT = SOURCE / 'captioned'
FONT = Path('/usr/share/fonts/truetype/dejavu')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    rows = re.findall(r'^\| (\d+) \| `([^`]+)` \| (.*?) \| Included \|$',
                      (ROOT / 'docs/figure-captions.md').read_text(), re.M)
    captions = {int(n): (name, text) for n, name, text in rows if int(n)}
    assert set(captions) == set(range(1, 27)), 'Expected figures 1–26'
    originals = sorted(SOURCE.glob('*.png'))
    assert len(originals) == 26
    protected = originals + list((ROOT / 'assets/architecture').glob('00_*.png'))
    before = {str(p.relative_to(ROOT)): digest(p) for p in protected}
    OUTPUT.mkdir(exist_ok=True)
    regular = ImageFont.truetype(str(FONT / 'DejaVuSans.ttf'), 24)
    bold = ImageFont.truetype(str(FONT / 'DejaVuSans-Bold.ttf'), 24)
    for n, (name, description) in captions.items():
        matches = list(SOURCE.glob(f'{n:02d}_*.png'))
        assert len(matches) == 1 and matches[0].name == name
        with Image.open(matches[0]) as source:
            original = source.convert('RGBA')
            width, height = original.size
            margin, leading = 32, 36
            # Use measured glyph widths, with a bold figure label and hanging wrap.
            tokens = [(f'Figure {n}:', bold)] + [(word, regular) for word in description.split()]
            lines, line, used = [], [], 0
            for word, font in tokens:
                advance = font.getlength(word + ' ')
                if line and used + advance > width - 2 * margin:
                    lines.append(line)
                    line, used = [], 0
                assert advance < width - 2 * margin
                line.append((word, font, used))
                used += advance
            lines.append(line)
            result = Image.new('RGBA', (width, height + 2 * margin + leading * len(lines)), 'white')
            result.paste(original, (0, 0))
            draw = ImageDraw.Draw(result)
            draw.line((0, height, width, height), fill='#d5dbe3', width=1)
            for row, words in enumerate(lines):
                for word, font, x in words:
                    draw.text((margin + x, height + margin + row * leading), word,
                              font=font, fill='#172b40', anchor='lt')
            metadata = PngImagePlugin.PngInfo()
            metadata.add_text('Caption', f'Figure {n}: {description}')
            result.save(OUTPUT / name, pnginfo=metadata)
            with Image.open(OUTPUT / name) as check:
                assert check.crop((0, 0, width, height)).tobytes() == original.tobytes()
                assert check.info['Caption'] == f'Figure {n}: {description}'
    assert all(digest(ROOT / p) == sha for p, sha in before.items())
    (OUTPUT / 'original-sha256.json').write_text(json.dumps(before, indent=2) + '\n')
    print('Verified 26 exact captions, unchanged screenshot pixels, and unchanged original/architecture hashes.')


if __name__ == '__main__':
    main()
