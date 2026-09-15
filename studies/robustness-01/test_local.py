"""Small arithmetic, preservation and tamper tests for this standalone study."""
import hashlib,itertools,json,math,sys,tarfile,unittest
from fractions import Fraction as F
from pathlib import Path
import numpy as np
import exact as ex
from exact import Q
from study import build
ROOT=Path(__file__).resolve().parent
with tarfile.open(ROOT/'EVIDENCE.tar.xz','r:xz') as a:
    RESULTS=json.loads(a.extractfile('RESULTS.json').read())

class StudyTests(unittest.TestCase):
    def test_complex_rational_arithmetic(self):
        x=Q(F(2,3),F(4,5));y=Q(F(7,11),F(-2,7))
        self.assertEqual((x*y)/y,x)
        self.assertEqual(x*x.conj(),Q(F(4,9)+F(16,25)))
        self.assertEqual(ex.mul(ex.mat([[x,y]]),ex.adj(ex.mat([[x,y]])))[0][0],x*x.conj()+y*y.conj())
    def test_two_by_two_exact_positivity(self):
        for a,b,r,i in itertools.product([F(1),F(2)],repeat=4):
            H=[[Q(a),Q(r,i)],[Q(r,-i),Q(b)]]
            self.assertEqual(ex.positive(H),a*b>r*r+i*i)
        self.assertFalse(ex.positive(ex.zeros()))
    def test_outward_rounding(self):
        for n in range(-100,101):
            x=F(n,137)
            self.assertLessEqual(F(ex.down(x)),x);self.assertGreaterEqual(F(ex.up(x)),x)
        for x in [F(1,3),F(1,10**40),F(5)]:self.assertGreaterEqual(ex.sqrt_upper(x)**2,x)
    def test_phase_and_rotation_models(self):
        for case in RESULTS['cases']:
            s=case['model'];A,A0,K,v,B,Rj=build(s)
            if s['kind']=='marked_phase':
                self.assertTrue(all(ex.mul(ex.adj(a),a)==ex.mul(ex.adj(A0[j]),A0[j]) for j,a in enumerate(A)))
            if s['kind']=='unitary':self.assertEqual(ex.mul(ex.adj(K),K),ex.eye())
    def test_bad_upper_and_measurement_rejected(self):
        c=RESULTS['cases'][3];A,A0,K,v,B,Rj=build(c['model']);J=c['joint']
        Y=ex.dec(J['dual_Y']);bad=ex.sub(Y,ex.scale(ex.eye(),F(1)))
        self.assertFalse(ex.positive(bad))
        Ms=[ex.mul(ex.dec(f),ex.adj(ex.dec(f))) for f in J['effect_factors']]
        sm=ex.zeros()
        for a in Ms:sm=ex.add(sm,a)
        self.assertFalse(ex.positive(ex.sub(ex.scale(ex.eye(),F(J['effect_scale'])/2),sm)))
    def test_archive_inventory_and_hashes(self):
        s=json.loads((ROOT/'SUMMARY.json').read_text())
        self.assertEqual(hashlib.sha256((ROOT/'EVIDENCE.tar.xz').read_bytes()).hexdigest(),s['evidence_sha256'])
        with tarfile.open(ROOT/'EVIDENCE.tar.xz','r:xz') as a:
            self.assertEqual(set(a.getnames()),set(s['evidence_members']))
            for n,h in s['evidence_members'].items():
                self.assertTrue(a.getmember(n).isfile());self.assertEqual(hashlib.sha256(a.extractfile(n).read()).hexdigest(),h)
    def test_document_math_and_control_characters(self):
        for p in ROOT.glob('*.md'):
            t=p.read_text()
            self.assertFalse(any(ord(x)<32 and x not in '\n\t' for x in t),p.name)
            self.assertEqual(t.count('$$')%2,0,p.name)
            self.assertNotIn('\\operatorname',t,p.name)
            self.assertFalse(any('$' in l for l in t.splitlines() if l.startswith('#')),p.name)
    def test_roles_and_limits_visible(self):
        report=(ROOT/'REPORT.md').read_text();proof=(ROOT/'PROOFS.md').read_text();work=(ROOT/'CALIBRATION_WORKSHEET.md').read_text()
        for phrase in ['pending','not laboratory evidence','arbitrary final']:
            self.assertIn(phrase,(report+proof).lower())
        for phrase in ['No field below','P0','P1','not acceptance','independent']:
            # Numeric fields are labelled NOT acceptance in uppercase in the worksheet.
            self.assertIn(phrase.lower(),work.lower())
        self.assertIn('No canonical',report)

if __name__=='__main__':unittest.main(verbosity=2)
