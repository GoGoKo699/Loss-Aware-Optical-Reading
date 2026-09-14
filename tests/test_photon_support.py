"""F01-F03 regressions; exact signs and independent 120-digit original equation."""
from fractions import Fraction
import importlib.util
import json
import math
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch
import mpmath as mp
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'src'),str(ROOT/'scripts')]
import theory
import photon_support as support
from verify_import import verify, CHANGE_RECORD


def truth(eta, penalty):
    """Original unscaled secular equation, not production's monotone residual."""
    with mp.workdps(120):
        def exact(x):
            n,d=float(x).as_integer_ratio()
            return mp.mpf(n)/d
        e=list(map(exact,eta)); L=exact(penalty); m=len(e)
        l0=mp.mpf(1)/(m-1); ell=max(L,l0)
        if len(set(e))==1:
            b=e[0]
        else:
            low=mp.mpf(0); high=max(e)
            for _ in range(420):
                b=(low+high)/2
                sign=(1+ell)/m*sum(x/(b+ell*x) for x in e)-1
                if sign>0:low=b
                else:high=b
            b=(low+high)/2
        if L<l0:b=(1+L)*(1+(m-1)*b)/m-L
        return +b


class PhotonSupportTests(unittest.TestCase):
    def assert_enclosure(self, eta, penalty):
        b=support.support_interval(eta,penalty)
        e=tuple(Fraction(float(x)) for x in eta)
        ell=Fraction(*b['effective_penalty_ratio'])
        lo=Fraction(b['branch_lower']);hi=Fraction(b['branch_upper'])
        # Independent sign of the ORIGINAL rational secular equation (decreasing).
        def original(x):return (1+ell)*sum((v/(x+ell*v) for v in e),Fraction())/len(e)-1
        self.assertGreaterEqual(original(lo),0)
        self.assertLessEqual(original(hi),0)
        self.assertTrue(lo==hi or math.nextafter(float(lo),math.inf)==float(hi))
        with mp.workdps(120):
            t=truth(eta,penalty)
            self.assertLessEqual(mp.mpf(b['lower']),t+mp.mpf('1e-95'))
            self.assertGreaterEqual(mp.mpf(b['upper']),t-mp.mpf('1e-95'))
        return b

    def test_reported_F02_counterexample(self):
        eta=[.2,.4,.8,.9]
        for lam in (1e12,1e14,1e15,1e16,1e17,1e18):
            b=self.assert_enclosure(eta,lam);v=theory.photon_score(eta,lam)
            self.assertLess(abs(v['score']-float(truth(eta,lam))),2e-15)
            self.assertEqual(v['score_upper'],b['upper'])
            self.assertGreaterEqual(Fraction(b['upper']),Fraction(4)/sum((1/Fraction(x) for x in eta),Fraction()))
            self.assertLess(abs(v['C']-lam*v['E']-v['score']),2e-15)
            self.assertGreaterEqual(v['E'],0)

    def test_random_exact_enclosures(self):
        rng=np.random.default_rng(202609140201)
        for m in (2,3,4,5,8,16):
            for k in range(3):
                eta=np.exp(rng.uniform(math.log(1e-12),0,m))
                for lam in (0.,1/(m-1),5.,1e18):
                    with self.subTest(m=m,k=k,penalty=lam):self.assert_enclosure(eta,lam)

    def test_extreme_domain_and_nearly_uniform(self):
        for eta in ([1e-12,1.],[1e-12,1e-12,1.,1.],[.7,math.nextafter(.7,1.)],np.linspace(.01,1,64)):
            for lam in (0.,5.,1e18):self.assert_enclosure(eta,lam)

    def test_uniform_root_is_exactly_enclosed(self):
        for m in (2,3,4,8):
            for eta in (1e-12,.7,1.):
                for lam in (0.,1/(m-1),1e18):self.assert_enclosure([eta]*m,lam)

    def test_penalty_boundary_neighbors(self):
        for m in (3,4,8):
            boundary=1/(m-1);eta=np.linspace(.2,.9,m)
            for lam in (math.nextafter(boundary,0.),boundary,math.nextafter(boundary,math.inf)):
                self.assert_enclosure(eta,lam)

    def test_nominal_recipe_and_pairwise_error(self):
        for lam in (0.,1/3,1.,5.,1e3):
            v=theory.photon_score([.7,.7,.7,.14],lam)
            self.assertAlmostEqual(sum(v['p']),1.)
            self.assertAlmostEqual(v['C']+v['E']+v['F'],1.)
            self.assertLess(abs(v['C']-lam*v['E']-v['score']),2e-12)
            a=np.sqrt(np.array([.7,.7,.7,.14])*v['p'])
            if lam>=1/3:
                pair=sum((a[i]-a[k])**2 for i in range(4) for k in range(i))/4
                self.assertLess(abs(pair-v['E']),1e-15)

    def test_unsupported_domain_rejected_by_all_score_callers(self):
        bad=[([.5],5),([.5]*65,5),([math.nextafter(1e-12,0),.5],5),
             ([.2,.5],math.nextafter(1e18,math.inf)),([.2,.5],-1),
             ([.2,.5],math.inf),([.2,.5],math.nan),([.2,math.nan],5)]
        for eta,lam in bad:
            with self.subTest(eta=eta,penalty=lam):
                with self.assertRaises(ValueError):theory.photon_score(eta,lam)
                with self.assertRaises(ValueError):support.support_interval(eta,lam)
                with self.assertRaises(ValueError):theory.certify_reverse_counts(dict(correct=1,wrong=0,inconclusive=0),lam,eta,0.,.05)

    def test_frontier_tiny_budget_fails_explicitly(self):
        with self.assertRaises(support.PhotonNumericalDomainError):
            theory.photon_frontier([.2,.4,.8,.9],1e-100)
        self.assertEqual(theory.photon_frontier([.2,.4,.8,.9],0.)['E'],0.)

    def test_reverse_caller_does_not_use_nominal_score(self):
        eta=[.2,.4,.8,.9];L=1e15
        with patch.object(theory,'photon_score',return_value={'score':-100.}):
            result=theory.certify_reverse_counts(dict(correct=100,wrong=0,inconclusive=0),L,eta,0.,.05)
        self.assertEqual(result['nominal_one_photon_upper'],support.support_interval(eta,L)['upper'])

    def test_reverse_addition_is_outward(self):
        for eta,lam,radius in [([.7,.7,.7,.035],5.,.003),([.2,.4,.8,.9],1e18,1e-30),([1.,1.],1.,1.)]:
            nominal,upper=support.reverse_support_upper(eta,lam,radius)
            exact=min(Fraction(1),Fraction(nominal)+2*(1+Fraction(lam))*Fraction(radius))
            self.assertGreaterEqual(Fraction(upper),exact)

    def test_rounding_directions(self):
        for q in (Fraction(1,3),Fraction(1,10),Fraction(0),Fraction(-1,3),Fraction.from_float(.7)):
            self.assertLessEqual(Fraction(support.outward_float(q,False)),q)
            self.assertGreaterEqual(Fraction(support.outward_float(q,True)),q)

    def test_F01_and_F03_text_repaired(self):
        text=(ROOT/'proofs/THEORY.md').read_text()
        self.assertIn('C-lambda E <= min{1, K_lambda[1-exp(-kappa mu)]}.',text)
        self.assertNotIn('C-lambda E <= K_lambda[1-exp(-kappa mu)] <= 1.',text)
        self.assertNotIn('positive-P mixtures',theory.classical_uniform_frontier.__doc__)
        self.assertIn('Glauber-Sudarshan',theory.classical_uniform_frontier.__doc__)

    def test_import_manifest_and_original_archive_stay_fixed(self):
        result=verify()
        self.assertTrue(result['original_import_manifest_unchanged'])
        self.assertTrue(result['source_archive_unchanged'])
        self.assertFalse(result['scientific_content_unchanged'])
        self.assertEqual(len(result['authorized_changes_verified']),4)

    def test_authorized_added_module_is_protected(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)/'repo'
            shutil.copytree(ROOT,root,ignore=shutil.ignore_patterns('.git','runs','__pycache__'))
            (root/'src/photon_support.py').write_text('# changed\n')
            with self.assertRaisesRegex(ValueError,'Protected added file changed'):verify(root)

    def test_change_ledger_cannot_omit_an_old_hash(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)/'repo'
            shutil.copytree(ROOT,root,ignore=shutil.ignore_patterns('.git','runs','__pycache__'))
            p=root/CHANGE_RECORD;j=json.loads(p.read_text());j['changes'][0]['old_sha256']='0'*64
            p.write_text(json.dumps(j))
            with self.assertRaisesRegex(ValueError,'previous hash'):verify(root)

    def test_original_manifest_cannot_be_rebaselined(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)/'repo'
            shutil.copytree(ROOT,root,ignore=shutil.ignore_patterns('.git','runs','__pycache__'))
            p=root/'provenance/IMPORT_MANIFEST.json';p.write_bytes(p.read_bytes()+b' ')
            with self.assertRaisesRegex(ValueError,'Original import manifest changed'):verify(root)

if __name__=='__main__':unittest.main()
