from pathlib import Path
import sys
import tempfile
import unittest
from zipfile import ZipFile

SCRIPTS = Path(__file__).resolve().parents[1] / 'skills/hjs_ppt/scripts'
sys.path.insert(0, str(SCRIPTS))
from extract_pptx_assets import extract
from find_asset import search

P = 'http://schemas.openxmlformats.org/presentationml/2006/main'
A = 'http://schemas.openxmlformats.org/drawingml/2006/main'
R = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
REL = 'http://schemas.openxmlformats.org/package/2006/relationships'


class AssetTests(unittest.TestCase):
    def fixture(self, path):
        pic = '<p:pic><p:nvPicPr><p:cNvPr id="4" name="Crop"/></p:nvPicPr><p:blipFill><a:blip r:embed="image"/><a:srcRect l="25000"/></p:blipFill></p:pic>'
        external = '<p:pic><p:blipFill><a:blip r:link="external"/></p:blipFill></p:pic>'
        with ZipFile(path, 'w') as z:
            z.writestr('ppt/presentation.xml', f'<p:presentation xmlns:p="{P}" xmlns:r="{R}"><p:sldIdLst><p:sldId r:id="s2"/><p:sldId r:id="s1"/></p:sldIdLst></p:presentation>')
            z.writestr('ppt/_rels/presentation.xml.rels', f'<Relationships xmlns="{REL}"><Relationship Id="s1" Target="slides/slide1.xml"/><Relationship Id="s2" Target="slides/slide2.xml"/></Relationships>')
            for n in (1,2):
                z.writestr(f'ppt/slides/slide{n}.xml', f'<p:sld xmlns:p="{P}" xmlns:a="{A}" xmlns:r="{R}"><p:cSld><p:spTree><p:grpSp>{pic}</p:grpSp>{external}<p:graphicFrame>{pic}</p:graphicFrame></p:spTree></p:cSld></p:sld>')
                z.writestr(f'ppt/slides/_rels/slide{n}.xml.rels', f'<Relationships xmlns="{REL}"><Relationship Id="image" Target="../media/image{n}.png"/><Relationship Id="external" Target="https://example.invalid/private.png" TargetMode="External"/></Relationships>')
                z.writestr(f'ppt/media/image{n}.png', b'same-image-bytes')

    def test_private_extraction_keeps_crops_order_bytes_and_skips_external_ole(self):
        with tempfile.TemporaryDirectory() as tmp:
            source, out = Path(tmp)/'source.pptx', Path(tmp)/'assets'
            self.fixture(source)
            before = source.read_bytes()
            result = extract(source, out)
            self.assertEqual(1, result['unique_files'])
            self.assertEqual(2, len(result['occurrences']))
            self.assertEqual('ppt/media/image2.png', result['occurrences'][0]['source_part'])
            self.assertEqual(.25, result['occurrences'][0]['crop_fraction']['l'])
            self.assertEqual(2, len(result['skipped']))
            self.assertEqual(b'same-image-bytes', (out/result['occurrences'][0]['file']).read_bytes())
            self.assertEqual(before, source.read_bytes())
            with self.assertRaises(FileExistsError): extract(source, out)

    def test_source_extraction_never_writes_to_installed_skill(self):
        with self.assertRaises(ValueError):
            extract('unused.pptx', SCRIPTS.parent/'assets'/'source-dump')

    def test_catalogue_search_returns_real_semantic_assets(self):
        for query, identity in [('相机','camera'),('network','neural-layers'),('局部','roi-magnifier')]:
            found = search(query)
            self.assertIn(identity, [x['id'] for x in found])
            self.assertTrue(all(Path(x['path']).is_file() for x in found))
            self.assertTrue(all(x['evidence'] is False for x in found))
        self.assertEqual([], search('nonexistent-asset-term'))


if __name__ == '__main__': unittest.main()
