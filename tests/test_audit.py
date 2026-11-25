import tempfile
import unittest
from pathlib import Path
from meid_validation_claim_audit.audit import audit, documentation_claims, source_evidence
from meid_validation_claim_audit.phrases import GENERIC_NAMES, MEIDVALIDATION, NOMEIDVALIDATION


class AuditTests(unittest.TestCase):
    def test_phrases(self):
        self.assertEqual((len(set(MEIDVALIDATION)), len(set(NOMEIDVALIDATION)), len(set(GENERIC_NAMES))), (50, 24, 24))
        for phrase in MEIDVALIDATION:
            with self.subTest(phrase=phrase): self.assertTrue(documentation_claims(phrase)[0])
        for phrase in NOMEIDVALIDATION:
            with self.subTest(phrase=phrase): self.assertEqual(documentation_claims(phrase), (False, True))
        self.assertEqual(documentation_claims('```\nvalidate meid\n```'), (False, False))
        self.assertEqual(documentation_claims('invalidated meid'), (False, False))

    def test_library_routes(self):
        for method in ('validate', 'is_valid'):
            for prefix, call in [('import stdnum.meid', 'stdnum.meid.'+method), ('import stdnum.meid as im', 'im.'+method), ('from stdnum import meid', 'meid.'+method), ('import stdnum', 'stdnum.meid.'+method), ('from stdnum.meid import '+method, method), ('from stdnum.meid import '+method+' as v', 'v')]:
                with self.subTest(prefix=prefix, method=method): self.assertTrue(source_evidence(prefix+'\n'+call+'(x)'))

    def test_generic_routes(self):
        for name in GENERIC_NAMES:
            for code in ('obj.'+name+'(x)', 'from other import '+name+' as f\nf(x)', 'obj = thing()\nobj.'+name+'(x)'):
                with self.subTest(code=code): self.assertTrue(source_evidence(code))

    def test_not_evidence(self):
        cases=['import stdnum.meid', 'validate(x)', 'is_valid(x)', 'meid(x)', 'validate_meid(x)', 'obj.validate(x)', 'obj.is_valid(x)', 'stdnum.meid.validate(x)', 'import stdnum.luhn\nstdnum.luhn.validate(x)', 'import stdnum.luhn\nstdnum.luhn.calc_check_digit(x)', 'import re\nre.match(x,y)', 'import re\nre.search(x,y)', 'import re\nre.fullmatch(x,y)', 'len(x)==14', 'x[:8] in manufacturers', 'imei.validate(x)', 'esn.validate(x)', 'obj.lookup_meid(x)', 'validators.meid(x)', '"validate meid"', '# validate meid', 'obj.validate_meid', 'def broken(:', 'import subprocess\nsubprocess.run(["validate_meid"])', 'from x import validate_meid\ndef validate_meid(x): pass\nvalidate_meid(x)', 'import stdnum.meid as im\nim = x\nim.validate(x)', 'import stdnum.meid as im\nwith x as im: pass\nim.validate(x)', 'class X:\n def validate_meid(self): pass\nobj.validate_meid(x)']
        cases += ['import stdnum.meid as m\nm.'+name+'(x)' for name in ('compact','format','calc_check_digit','to_binary','to_pseudo_esn')]
        cases += ['obj.'+name+'(x)' for name in ('meid','compact','format','calc_check_digit','to_binary','to_pseudo_esn')]
        for code in cases:
            with self.subTest(code=code): self.assertFalse(source_evidence(code))

    def test_findings(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d); (p/'README.md').write_text('validate meid')
            self.assertEqual(audit(p)[0]['severity'], 'HIGH')
            (p/'tests').mkdir(); (p/'tests/test_x.py').write_text('obj.validate_meid(x)')
            self.assertEqual(audit(p)[0]['severity'], 'MEDIUM')
            (p/'main.py').write_text('obj.validate_meid(x)')
            self.assertEqual(audit(p), [])
            (p/'README.md').write_text('does not validate meid')
            self.assertEqual(audit(p)[0]['severity'], 'HIGH')
            (p/'main.py').unlink(); self.assertEqual(audit(p), [])

    def test_exclusions(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d); (p/'README.md').write_text('validate meid')
            for folder in ('fixtures','docs','examples'):
                (p/folder).mkdir(); (p/folder/'x.py').write_text('obj.validate_meid(x)')
            (p/'target').mkdir(); (p/'target/x.py').write_text('obj.validate_meid(x)')
            self.assertEqual(audit(p, ['target'])[0]['severity'], 'HIGH')
            (p/'link').symlink_to(p/'target', target_is_directory=True)
            self.assertEqual(audit(p, ['target'])[0]['severity'], 'HIGH')
