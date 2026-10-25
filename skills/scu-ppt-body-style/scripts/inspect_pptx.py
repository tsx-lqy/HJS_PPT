"""Read slide text, notes and native-object counts. No rendering or source edits.

Python 3.10+, standard library only. JSON to stdout; exit 1 for parse errors or
missing internal relationship targets. This is a scoped inventory, not a full
Open XML conformance, math, data, or visual validator.
"""

import argparse
import json
import posixpath
import sys
from pathlib import Path
from urllib.parse import unquote
from zipfile import BadZipFile, ZipFile
import xml.etree.ElementTree as ET

NS = {
    'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    'c': 'http://schemas.openxmlformats.org/drawingml/2006/chart',
    'm': 'http://schemas.openxmlformats.org/officeDocument/2006/math',
}


def target_path(part, target):
    """Resolve a package relationship relative to its owning part."""
    path = unquote(target.split('#', 1)[0])
    return posixpath.normpath(posixpath.join(posixpath.dirname(part), path)).lstrip('/')


def relationships(archive, part):
    parent, filename = posixpath.split(part)
    name = posixpath.join(parent, '_rels', filename + '.rels')
    if name not in archive.namelist():
        return {}
    return {e.get('Id'): e.attrib for e in ET.fromstring(archive.read(name))}


def notes_text(root):
    paragraphs = []
    for shape in root.findall('.//p:sp', NS):
        placeholder = shape.find('p:nvSpPr/p:nvPr/p:ph', NS)
        if placeholder is not None and placeholder.get('type') in {'sldNum', 'dt', 'hdr', 'ftr'}:
            continue
        for paragraph in shape.findall('.//a:p', NS):
            text = ''.join(node.text or '' for node in paragraph.findall('.//a:t', NS))
            if text.strip():
                paragraphs.append(text)
    return '\n'.join(paragraphs)


def inspect(path, include_text=False):
    with ZipFile(path) as archive:
        names = set(archive.namelist())
        missing = []
        for name in sorted(n for n in names if n.endswith('.rels')):
            if name == '_rels/.rels':
                owner = ''
            else:
                parent, leaf = name.rsplit('/_rels/', 1)
                owner = parent + '/' + leaf[:-5]
            for rel in ET.fromstring(archive.read(name)):
                if rel.get('TargetMode') == 'External':
                    continue
                target = target_path(owner, rel.get('Target', ''))
                if target not in names:
                    missing.append({'owner': owner, 'id': rel.get('Id'), 'target': target})

        presentation = ET.fromstring(archive.read('ppt/presentation.xml'))
        links = relationships(archive, 'ppt/presentation.xml')
        size = presentation.find('p:sldSz', NS)
        slides = []
        for number, item in enumerate(presentation.findall('p:sldIdLst/p:sldId', NS), 1):
            rel = links[item.get('{' + NS['r'] + '}id')]
            part = target_path('ppt/presentation.xml', rel['Target'])
            root = ET.fromstring(archive.read(part))
            slide_links = relationships(archive, part)
            notes = ''
            for link in slide_links.values():
                if link.get('Type', '').endswith('/notesSlide') and link.get('TargetMode') != 'External':
                    note_part = target_path(part, link['Target'])
                    if note_part in names:
                        notes = notes_text(ET.fromstring(archive.read(note_part)))
            row = {
                'number': number, 'part': part, 'hidden': root.get('show') in {'0', 'false'},
                'math_objects': len(root.findall('.//m:oMath', NS)),
                'chart_references': len(root.findall('.//c:chart', NS)),
                'tables': len(root.findall('.//a:tbl', NS)),
                'pictures': len(root.findall('.//p:pic', NS)),
                'has_notes_text': bool(notes.strip()),
            }
            if include_text:
                row['text'] = '\n'.join(''.join(n.text or '' for n in p.findall('.//a:t', NS))
                                        for p in root.findall('.//a:p', NS))
                row['notes'] = notes
            slides.append(row)
        return {
            'file': Path(path).name,
            'slide_count': len(slides),
            'size_emu': dict(size.attrib) if size is not None else None,
            'slides': slides,
            'missing_internal_targets': missing,
            'scope': 'Slide-local XML inventory only; no image OCR, math/data validation, or visual review.',
        }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pptx', type=Path)
    parser.add_argument('--text', action='store_true', help='Include slide-local text and speaker notes.')
    args = parser.parse_args()
    try:
        report = inspect(args.pptx, args.text)
    except (OSError, BadZipFile, ET.ParseError, KeyError, ValueError) as error:
        print(f'Cannot inspect PPTX: {error}', file=sys.stderr)
        return 1
    # UTF-8 avoids machine-default encoding changing exported Chinese text.
    sys.stdout.reconfigure(encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return int(bool(report['missing_internal_targets']))


if __name__ == '__main__':
    raise SystemExit(main())
