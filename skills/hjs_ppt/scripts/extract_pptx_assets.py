"""Extract slide-local pictures into a NEW private task directory (Python 3.10+).

Keeps source bytes, real slide order, crop fractions and placement. Does not
render groups, OCR, fetch external images, or authorize public redistribution.
"""
import argparse
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET
from zipfile import ZipFile

from inspect_pptx import NS, relationships, target_path


def slide_pictures(container):
    for child in container:
        if child.tag == '{' + NS['p'] + '}pic':
            yield child
        elif child.tag == '{' + NS['p'] + '}grpSp':
            yield from slide_pictures(child)


def extract(source, destination):
    source, destination = Path(source).resolve(), Path(destination).resolve()
    skill_dir = Path(__file__).resolve().parents[1]
    if destination == skill_dir or skill_dir in destination.parents:
        raise ValueError('Use a task directory outside the installed skill.')
    if destination.exists():
        raise FileExistsError('Choose a new output directory; existing files are never overwritten.')
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    records, blobs, skipped = [], {}, []
    with ZipFile(source) as archive:
        presentation = ET.fromstring(archive.read('ppt/presentation.xml'))
        links = relationships(archive, 'ppt/presentation.xml')
        for page, item in enumerate(presentation.findall('p:sldIdLst/p:sldId', NS), 1):
            part = target_path('ppt/presentation.xml', links[item.get('{' + NS['r'] + '}id')]['Target'])
            root = ET.fromstring(archive.read(part))
            slide_links = relationships(archive, part)
            # Only shape-tree pictures, excluding OLE fallback previews.
            for picture in slide_pictures(root.find('p:cSld/p:spTree', NS)):
                info = picture.find('p:nvPicPr/p:cNvPr', NS)
                blip = picture.find('p:blipFill/a:blip', NS)
                if blip is None:
                    continue
                rid = blip.get('{' + NS['r'] + '}embed') or blip.get('{' + NS['r'] + '}link')
                rel = slide_links.get(rid, {})
                identity = {'slide': page, 'shape_name': info.get('name', '') if info is not None else ''}
                if rel.get('TargetMode') == 'External' or not rel.get('Target'):
                    skipped.append({**identity, 'reason': 'external_or_missing_relationship'})
                    continue
                media = target_path(part, rel['Target'])
                if not media.startswith('ppt/media/'):
                    skipped.append({**identity, 'reason': 'not_package_media'})
                    continue
                data = archive.read(media)
                sha = hashlib.sha256(data).hexdigest()
                suffix = Path(media).suffix.lower()
                if suffix not in {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tif', '.tiff', '.emf', '.wmf', '.svg'}:
                    skipped.append({**identity, 'reason': 'unsupported_media_type'})
                    continue
                name = f'{sha}{suffix}'
                blobs[name] = data
                crop = picture.find('p:blipFill/a:srcRect', NS)
                transform = picture.find('p:spPr/a:xfrm', NS)
                records.append({**identity, 'file': name, 'sha256': sha,
                    'source_part': media, 'hidden_slide': root.get('show') in {'0', 'false'},
                    'crop_fraction': {key: int(crop.get(key, '0')) / 100000 for key in ('l','t','r','b')} if crop is not None else {},
                    'transform_xml': ET.tostring(transform, encoding='unicode') if transform is not None else None,
                    'reuse': 'private_source_unreviewed',
                    'note': 'Original full image; crop, group transforms, rotations and scientific meaning require visual review.'})
    destination.mkdir(parents=True)
    for name, data in blobs.items():
        (destination / name).write_bytes(data)
    manifest = {'source_name': source.name, 'source_sha256': digest,
        'unique_files': len(blobs), 'occurrences': records, 'skipped': skipped,
        'scope': 'slide-local pictures only; no masters, layouts, native groups, charts or MathType objects'}
    (destination / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    if hashlib.sha256(source.read_bytes()).hexdigest() != digest:
        raise RuntimeError('Source changed during extraction.')
    return manifest


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    result = extract(args.input, args.output)
    print(json.dumps({'unique_files': result['unique_files'], 'occurrences': len(result['occurrences']), 'skipped': len(result['skipped'])}))
