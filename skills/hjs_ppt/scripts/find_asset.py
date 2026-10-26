"""Search the bundled semantic asset catalogue, without additional packages."""
import argparse
import json
from pathlib import Path


def search(query, root=None):
    root = Path(root) if root else Path(__file__).resolve().parents[1] / 'assets'
    catalog = json.loads((root / 'catalog.json').read_text(encoding='utf-8'))
    words = query.casefold().split()
    found = []
    for item in catalog['assets']:
        haystack = ' '.join([item['id'], item['title'], item['use'], *item['tags']]).casefold()
        score = sum(word in haystack for word in words)
        if not words or score:
            found.append({**item, 'path': str((root / item['file']).resolve()), 'score': score})
    return sorted(found, key=lambda item: (-item['score'], item['id']))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('query', nargs='?', default='')
    args = parser.parse_args()
    print(json.dumps(search(args.query), ensure_ascii=False, indent=2))
