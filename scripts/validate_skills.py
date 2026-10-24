"""Validate this repository's skill packages using only the Python standard library."""

from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


def validate(root=ROOT):
    errors = []
    entries = sorted((root / 'skills').glob('*/SKILL.md'))
    if not entries:
        errors.append('No skills/<name>/SKILL.md files found.')
    for entry in entries:
        content = entry.read_text(encoding='utf-8')
        header = re.match(r'\A---\n(.*?)\n---\n', content, re.S)
        if not header:
            errors.append(f'{entry.relative_to(root)}: missing YAML frontmatter.')
            continue
        name = re.search(r'^name:\s*([a-z0-9]+(?:-[a-z0-9]+)*)\s*$', header[1], re.M)
        desc = re.search(r'^description:\s*(\S[^\n]*)$', header[1], re.M)
        if not name or name[1] != entry.parent.name or len(name[1]) > 64:
            errors.append(f'{entry.relative_to(root)}: name must match its directory.')
        if not desc or len(desc[1]) > 1024:
            errors.append(f'{entry.relative_to(root)}: require a single-line description of 1–1024 characters.')
        if re.search(r'\[TODO:|\[TBD:', content):
            errors.append(f'{entry.relative_to(root)}: unfinished scaffold.')
    docs = [*root.glob('*.md'), *(root / 'skills').rglob('*.md')]
    links = 0
    for doc in docs:
        content = doc.read_text(encoding='utf-8')
        if re.search(r'\b[A-Za-z]:[\\/](?:Users|SCUing)[\\/]', content):
            errors.append(f'{doc.relative_to(root)}: machine-specific path in public document.')
        for target in re.findall(r'!?\[[^\]]*\]\(([^)\s]+)\)', content):
            if re.match(r'^[a-z][a-z0-9+.-]*:', target, re.I) or target.startswith('#'):
                continue
            dest = (doc.parent / target.split('#')[0]).resolve()
            links += 1
            if not dest.is_relative_to(root.resolve()) or not dest.exists():
                errors.append(f'{doc.relative_to(root)}: broken or external local link {target}.')
    svgs = sorted((root / 'skills').rglob('*.svg'))
    for svg in svgs:
        try:
            element = ET.parse(svg).getroot()
            if element.tag != '{http://www.w3.org/2000/svg}svg' or not element.get('viewBox'):
                errors.append(f'{svg.relative_to(root)}: require SVG root and viewBox.')
            if any(e.tag.rsplit('}', 1)[-1] in {'script', 'image', 'foreignObject'} for e in element.iter()):
                errors.append(f'{svg.relative_to(root)}: reference diagrams must remain self-contained vectors.')
        except ET.ParseError as error:
            errors.append(f'{svg.relative_to(root)}: invalid XML: {error}.')
    for file in (root / 'skills').rglob('*'):
        if file.is_file() and file.name != 'LICENSE' and file.suffix not in {'.md', '.yaml', '.svg'}:
            errors.append(f'{file.relative_to(root)}: unexpected public skill resource type.')
    if not (root / 'LICENSE').is_file():
        errors.append('LICENSE is missing.')
    return errors, len(entries), links, len(svgs)


if __name__ == '__main__':
    errors, skills, links, svgs = validate()
    if errors:
        print('\n'.join(f'ERROR: {error}' for error in errors))
        sys.exit(1)
    print(f'PASS: {skills} skill(s), {links} local links, {svgs} SVG diagrams.')
