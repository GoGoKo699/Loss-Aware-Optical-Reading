"""Focused predecessor-translation checks, not a novelty proof or full scientific audit.

Run from a repository checkout with --source-root ., or against the hash-matched
selected-source repair package. No network. No writes to source or frozen results.
All arrays below implement the comparison derivations independently.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib
import json
import math
import os
import platform
import sys
from collections import Counter
from pathlib import Path
import numpy as np
import scipy

BASELINE = '80c73751806f45411251711bcfb6bccebc887f0a'
BLOBS = {'src/theory.py': 'e038afe2a21c6e54e3fc6eaccfbcb07c9de3ff60',
         'src/photon_support.py': '133f2b8cb6c41edf6ec873740b58c04eb94e632b',
         'proofs/THEORY.md': 'daa095381a2c21f1a9a9f660fe68cd8354e56bd6'}
SEED = 2026091501


def blob(data: bytes) -> str:
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def root_psd(a: np.ndarray, inverse: bool = False) -> np.ndarray:
    values, basis = np.linalg.eigh((a + a.conj().T)/2)
    if np.min(values) <= 0 and inverse:
        raise ArithmeticError('comparison requires strictly positive Gram matrix')
    factors = 1/np.sqrt(values) if inverse else np.sqrt(np.maximum(0, values))
    return (basis * factors) @ basis.conj().T


def four_family(theta: float) -> np.ndarray:
    e = np.exp(1j*theta)
    return np.array([[1,1,1,1], [1,e,-1,-e], [1,-1,1,-1], [1,-e,-1,e]], complex)


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source-root', type=Path, default=Path(__file__).resolve().parents[2])
    p.add_argument('--output', type=Path, required=True, help='New directory, never reused')
    args = p.parse_args()
    source = args.source_root.resolve()
    before = {name: (source/name).read_bytes() for name in BLOBS}
    for name, expected in BLOBS.items():
        if blob(before[name]) != expected:
            raise ValueError('Not the pinned repaired source: '+name)
    out = args.output.resolve()
    if out.exists() or out == source or (source/'src') in out.parents:
        raise ValueError('Output must be a new non-source directory')
    frozen = source/'results'
    if out == frozen or (frozen in out.parents and source/'results/runs' not in out.parents):
        raise ValueError('Do not overwrite frozen results')
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(source/'src'))
    theory = importlib.import_module('theory')
    rng = np.random.default_rng(SEED)
    checks: list[dict] = []
    examples: dict = {}

    def check(group: str, name: str, residual: float, tolerance: float = 1e-9) -> None:
        residual = float(residual)
        if not math.isfinite(residual) or residual < 0:
            raise AssertionError((group, name, residual))
        checks.append({'group':group, 'name':name, 'residual':residual, 'tolerance':tolerance})
        if residual > tolerance:
            raise AssertionError(checks[-1])

    # R1: existing SRM criterion, then its specialization to flat orthogonal codes.
    codes = [('four_one_flip', np.ones((4,4))-2*np.eye(4))]
    for m in (2,3,4,5,8):
        i=np.arange(m)
        codes.append((f'fourier_{m}', np.exp(2j*np.pi*np.outer(i,i)/m)))
    for t in (0.13,0.57,1.17):
        codes.append((f'complex_hadamard_{t}',four_family(t)))
    for code_name, Z in codes:
        m=len(Z); U=Z/np.sqrt(m)
        check('srm',code_name+'_unitary',np.max(abs(U.conj().T@U-np.eye(m))))
        for case in range(5):
            eta=rng.uniform(.03,.95,m); p0=rng.dirichlet(np.ones(m)*2); q=eta*p0
            Phi=np.diag(np.sqrt(q))@Z
            G=Phi.conj().T@Phi
            S=root_psd(G)
            M=Phi@root_psd(G,inverse=True)
            check('srm',f'{code_name}_{case}_measurement',np.max(abs(M-U)))
            diag_expected=np.sum(np.sqrt(q))/np.sqrt(m)
            check('srm',f'{code_name}_{case}_constant_diagonal',np.max(abs(np.diag(S)-diag_expected)))
            C=float(np.mean(abs(np.diag(M.conj().T@Phi))**2))
            check('srm',f'{code_name}_{case}_success',abs(C-np.sum(np.sqrt(q))**2/m))
            # R2: zero-error endpoint is the usual minimum coefficient/eigenvalue.
            success=m*float(q.min())
            residual=G-success*np.eye(m)
            check('usd',f'{code_name}_{case}_gram_minimum',abs(np.linalg.eigvalsh(G)[0]-success))
            check('usd',f'{code_name}_{case}_feasible',max(0,-np.linalg.eigvalsh(residual)[0]))
            p_inv=(1/eta)/np.sum(1/eta)
            H=m/np.sum(1/eta)
            check('usd',f'{code_name}_{case}_harmonic_mean',np.max(abs(eta*p_inv-H/m)))
            # R3: input/filter normalization exposes the scope difference.
            lam=5.; filtering=rng.uniform(.05,1,m)
            a=float(p0@filtering); pp=p0*filtering/a
            qf=q*filtering
            C_f=np.sum(np.sqrt(qf))**2/m; E_f=qf.sum()-C_f
            C_r=np.sum(np.sqrt(eta*pp))**2/m; E_r=(eta*pp).sum()-C_r
            score_f=C_f-lam*E_f; score_r=C_r-lam*E_r
            check('input_filter',f'{code_name}_{case}_normalization',abs(score_r*a-score_f))
            if score_f >= 0:
                check('input_filter',f'{code_name}_{case}_dominates',max(0,score_f-score_r))
            opt=theory.photon_score(eta,lam)
            vv=np.sqrt(eta)
            direct=float(np.linalg.eigvalsh((1+lam)*np.outer(vv,vv)/m-lam*np.diag(eta))[-1])
            check('input_filter',f'{code_name}_{case}_support',abs(opt['score']-direct))

    # R4: Herzog Eq (4.18) -> the repository's uniform four-state classical curve.
    translations=[]
    for x in (.001,.07,.7,1.,3.,6.):
        c=math.exp(-x); b=(1-c)/4; a=(1+3*c)/4
        for frac in np.linspace(0,1,13):
            F=float(frac*c)
            C=(math.sqrt(max(0,a-F))+3*math.sqrt(b))**2/4
            E=max(0,1-F-C)
            target=theory.classical_uniform_frontier(x,E)
            check('herzog',f'{x}_{frac}_rates',max(abs(C-target['C']),abs(F-target['F'])))
            check('herzog',f'{x}_{frac}_identity',abs((math.sqrt(C)-math.sqrt(E/3))**2-(1-c)))
        Cme=(math.sqrt(1+3*c)+3*math.sqrt(1-c))**2/16
        translations.append({'x':x,'constant_overlap':c,'ME_success':Cme,'USD_success':1-c})
    examples['uniform_endpoints']=translations

    # R5: binary spectral-contrast construction is exactly Bouchet et al. Eq (3).
    for case in range(20):
        m=4
        maps=[]
        for _ in range(2):
            A=rng.normal(size=(m,m))+1j*rng.normal(size=(m,m))
            A*=rng.uniform(.3,.95)/np.linalg.norm(A,2); maps.append(A)
        A0,A1=maps
        Diff=A1-A0; D=Diff.conj().T@Diff
        H,k=theory.contrast_operator(np.array(maps))
        check('binary_contrast',f'{case}_matrix',np.max(abs(2*H-D)))
        energy=rng.uniform(.03,2)
        dmax=float(np.linalg.eigvalsh(D)[-1]); c=math.exp(-k*energy)
        known=.5*(1+math.sqrt(-math.expm1(-energy*dmax)))
        derived=.5*(1+math.sqrt(max(0,1-c*c)))
        check('binary_contrast',f'{case}_Helstrom',abs(known-derived))

    # R6: displaced one-flip code has the PPM Hilbert-space Gram matrix.
    for case in range(12):
        q=rng.uniform(.01,1,4); amplitude=np.sqrt(q)*np.exp(1j*rng.uniform(-np.pi,np.pi,4))
        Z=np.ones((4,4))-2*np.eye(4)
        old=(amplitude[:,None]*Z).T
        new=old-amplitude[None,:]
        def gram(states):
            norms=np.sum(abs(states)**2,axis=1)
            return np.exp(-(norms[:,None]+norms[None,:])/2+states.conj()@states.T)
        a=np.exp(-2*q); formula=np.diag(1-a*a)+np.outer(a,a)
        check('nulling',f'{case}_original_gram',np.max(abs(gram(old)-formula)))
        check('nulling',f'{case}_displaced_gram',np.max(abs(gram(new)-formula)))
        check('nulling',f'{case}_PPM_amplitudes',np.max(abs(new+2*np.diag(amplitude))))

    # R7: the nulling receiver is not the arbitrary-POVM optimum at all energies.
    # This exhibits why a mean-energy proof must treat the second branch.
    def B(r,x):
        if r <= math.exp(-4*x/3): return .75*(-math.expm1(-4*x/3))
        ell=math.exp((math.log(r)-4*r*x)/(1+3*r))
        return 1-(3+1/r)*ell/4
    r=.01; x=3.; a=np.array([math.exp(-2*x/3)]*3+[1.])
    delta=max(0,2*a.max()-a.sum())
    global_fixed=(4-float(a@a)+delta*delta)/4
    extra=1-1.5*math.exp(-2*x/3)+1.5*math.exp(-4*x/3)
    check('high_energy','extra_branch_identity',abs(global_fixed-extra))
    check('high_energy','extra_strictly_exceeds_nulling',max(0, B(r,x)+.05-extra))
    # Exact upper/lower construction for this one sample, not a new general proof.
    dom=3; T=float(a[:3].sum())
    f=a*a+delta*a; f[dom]=a[dom]*T
    G=np.diag(1-a*a)+np.outer(a,a)
    residual=G-np.diag(1-f)
    check('high_energy','USD_feasibility',max(0,-np.linalg.eigvalsh(residual)[0]))
    check('high_energy','failure_probabilities',max(0,-float(f.min()),float(f.max())-1))
    check('high_energy','achieved_score',abs((1-f).mean()-extra))
    # A sampled comparison of the known supporting line, not proof about infinite support.
    mean=.7
    B0=B(r,mean); slope=math.exp(-4*mean/3)
    tangent_at_x=B0+slope*(x-mean)
    check('high_energy','mean_budget_line',max(0,extra-tangent_at_x))
    examples['high_energy_scope']={'r':r,'effective_pulse_energy':x,
        'optimized_nulling_receiver':B(r,x),'feasible_arbitrary_POVM':extra,
        'mean_effective_budget':mean,'mean_budget_supporting_line_at_pulse':tangent_at_x}
    examples['known_reversal']={'transmission':.7,
        'photon_USD':.7,'classical_USD':1-math.exp(-.7),
        'photon_ME':.7+.3/4,'classical_ME':translations[2]['ME_success']}

    for name, data in before.items():
        if (source/name).read_bytes() != data: raise AssertionError('Source changed: '+name)
    result={'status':'PASS','seed':SEED,'baseline_commit':BASELINE,
            'checks':len(checks),'groups':dict(Counter(c['group'] for c in checks)),
            'max_residual':max(c['residual'] for c in checks),
            'source_git_blobs':BLOBS,'source_bytes_unchanged':True,
            'scope':'Equation/normalization/measurement translations only. Not proof of originality; not a rerun of the full theory audit.',
            'ledger':checks,'examples':examples}
    env={'python':sys.version,'numpy':np.__version__,'scipy':scipy.__version__,
         'platform':platform.platform(),'network_used_by_script':False,
         'external_article_code_imported':False,'laboratory_data_used':False,
         'source_root':str(source),'working_tree':'archive-based hash-matched selected source; no authenticated local Git clone'}
    out.mkdir(parents=True,exist_ok=False)
    (out/'RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    (out/'ENVIRONMENT.json').write_text(json.dumps(env,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('status','checks','groups','max_residual','examples')},indent=2))

if __name__=='__main__':main()
