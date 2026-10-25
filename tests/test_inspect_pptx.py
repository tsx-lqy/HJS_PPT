"""Scoped XML fixtures exercise intake semantics; these are not rendered decks."""
import importlib.util
from pathlib import Path
import tempfile
import unittest
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('inspector', ROOT / 'skills/hjs_ppt/scripts/inspect_pptx.py')
inspector = importlib.util.module_from_spec(spec)
spec.loader.exec_module(inspector)
P = inspector.NS['p']
A = inspector.NS['a']
R = inspector.NS['r']
REL = 'http://schemas.openxmlformats.org/package/2006/relationships'


def rels(items):
    return '<Relationships xmlns="' + REL + '">' + ''.join(items) + '</Relationships>'


class IntakeTests(unittest.TestCase):
    def fixture(self, missing=False):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        path = Path(temp.name) / '输入.pptx'
        with ZipFile(path, 'w') as archive:
            archive.writestr('ppt/presentation.xml', f'<p:presentation xmlns:p="{P}" xmlns:r="{R}"><p:sldSz cx="100" cy="50"/><p:sldIdLst><p:sldId r:id="b"/><p:sldId r:id="a"/></p:sldIdLst></p:presentation>')
            archive.writestr('ppt/_rels/presentation.xml.rels', rels([
                '<Relationship Id="a" Target="slides/slide1.xml"/>',
                '<Relationship Id="b" Target="slides/slide9.xml"/>']))
            for name, label, hidden in [('slide1', '第二页', '1'), ('slide9', '第一页', '0')]:
                archive.writestr(f'ppt/slides/{name}.xml', f'<p:sld xmlns:p="{P}" xmlns:a="{A}" show="{hidden}"><a:p><a:r><a:t>{label}</a:t></a:r></a:p></p:sld>')
            archive.writestr('ppt/slides/_rels/slide9.xml.rels', rels([
                f'<Relationship Id="n" Type="{R}/notesSlide" Target="../notesSlides/notes%20one.xml"/>',
                '<Relationship Id="h" Target="https://example.org" TargetMode="External"/>',
                '<Relationship Id="i" Target="../media/missing.png"/>' if missing else '',
            ]))
            archive.writestr('ppt/notesSlides/notes one.xml', f'<p:notes xmlns:p="{P}" xmlns:a="{A}"><p:sp><p:nvSpPr><p:nvPr><p:ph type="sldNum"/></p:nvPr></p:nvSpPr><a:p><a:r><a:t>99</a:t></a:r></a:p></p:sp><p:sp><a:p><a:r><a:t>看右图，然后解释。</a:t></a:r></a:p></p:sp></p:notes>')
        return path

    def test_real_slide_order_hidden_flag_and_chinese_notes(self):
        report = inspector.inspect(self.fixture(), True)
        self.assertEqual([s['text'] for s in report['slides']], ['第一页', '第二页'])
        self.assertTrue(report['slides'][0]['hidden'])
        self.assertEqual(report['slides'][0]['notes'], '看右图，然后解释。')
        self.assertFalse(report['slides'][1]['has_notes_text'])
        self.assertEqual(report['missing_internal_targets'], [])

    def test_reports_broken_internal_target_but_not_external_link(self):
        report = inspector.inspect(self.fixture(missing=True))
        self.assertEqual(report['missing_internal_targets'], [
            {'owner': 'ppt/slides/slide9.xml', 'id': 'i', 'target': 'ppt/media/missing.png'}])
        self.assertNotIn('text', report['slides'][0])

    def test_page_number_alone_is_not_a_speaker_note(self):
        xml = f'<p:notes xmlns:p="{P}" xmlns:a="{A}"><p:sp><p:nvSpPr><p:nvPr><p:ph type="sldNum"/></p:nvPr></p:nvSpPr><a:p><a:r><a:t>12</a:t></a:r></a:p></p:sp></p:notes>'
        self.assertEqual(inspector.notes_text(inspector.ET.fromstring(xml)), '')

    def test_counts_native_math_chart_table_and_picture_separately(self):
        path = self.fixture()
        # Add object markup to the second slide, preserving a single part entry.
        with ZipFile(path) as archive:
            parts = {name: archive.read(name) for name in archive.namelist()}
        extra = (f'<m:oMath xmlns:m="{inspector.NS["m"]}"/>'
                 f'<c:chart xmlns:c="{inspector.NS["c"]}"/>'
                 '<a:tbl/><p:pic/>')
        parts['ppt/slides/slide1.xml'] = parts['ppt/slides/slide1.xml'].replace(b'</p:sld>', (extra+'</p:sld>').encode())
        with ZipFile(path, 'w') as archive:
            for name, data in parts.items():
                archive.writestr(name, data)
        row = inspector.inspect(path)['slides'][1]
        self.assertEqual([row[k] for k in ('math_objects','chart_references','tables','pictures')], [1,1,1,1])


if __name__ == '__main__':
    unittest.main()
