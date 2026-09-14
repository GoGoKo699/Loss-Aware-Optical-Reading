"""Independent checks of predecessor reductions, not a proof of priority.

No canonical module, external article code, optical hardware, or network is used.
Run: python comparison_checks.py --output <new-directory>
Universal conclusions depend on REDUCTIONS.md, not these finite examples.
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import platform
import sys
import numpy as np

BASELINE = 'db17e1ec1868107b0fe1042d5a480769b552633e'
SEED = 2026091502
TOL = 2e-10


def psdroot(matrix: np.ndarray) -> np.ndarray:
    eig, vec = np.linalg.eigh((matrix + matrix.conj().T)/2)
    if eig.min() < -1e-11:
        raise ArithmeticError('Matrix is not positive semidefinite')
    return (vec * np.sqrt(np.maximum(eig, 0))) @ vec.conj().T


def unitary(rng, m):
    a = rng.normal(size=(m, m)) + 1j*rng.normal(size=(m, m))
    q, r = np.linalg.qr(a)
    phase = np.diag(r)
    return q * (phase / abs(phase)).conj()


def offsum(matrix):
    return float(np.sum(abs(matrix)) - np.sum(abs(np.diag(matrix))))


def h(m, p):
    if not -1e-12 <= p <= 1+1e-12:
        raise ValueError('Invalid probability')
    p = min(1., max(0., p))
    return (m-2)*(1-p) + 2*math.sqrt(max(0., (m-1)*p*(1-p)))


def upper(m, R, E):
    return (math.sqrt(max(0., 1-R))+math.sqrt(max(0., E)/(m-1)))**2


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    out = args.output.resolve()
    if out.exists():
        parser.error('Output must be a new directory')
    # Do not permit output under canonical repository source/evidence directories.
    for root in [Path.cwd(), *Path(__file__).resolve().parents]:
        if (root/'AGENTS.md').is_file() and (root/'proofs').is_dir():
            for folder in ('src', 'proofs', 'baseline', 'provenance', 'templates', 'experiment'):
                protected = root/folder
                if out == protected or protected in out.parents:
                    parser.error('Output would write under a protected directory')
            frozen = root/'results'
            runs = frozen/'runs'
            if (out == frozen or out == runs or (frozen in out.parents and runs not in out.parents)):
                parser.error('Output must not write into frozen results')
    script_hash = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    rng = np.random.default_rng(SEED)
    checks, examples = [], {}

    def check(group, name, residual, tolerance=TOL):
        residual = float(residual)
        row = dict(group=group, name=name, residual=residual, tolerance=tolerance)
        checks.append(row)
        if not math.isfinite(residual) or not 0 <= residual <= tolerance:
            raise AssertionError(row)

    # S20: ordered root-overlap sum and zero-error uniform specialization.
    for m in (2, 3, 4, 8):
        for c in (0., .1, .5, .95):
            G = (1-c)*np.eye(m) + c*np.ones((m,m))
            phi = psdroot(G)
            conclusive = math.sqrt(1-c)*np.linalg.inv(phi)
            fail = np.eye(m)-conclusive.conj().T@conclusive
            C = float(np.trace((conclusive@phi).conj().T@(conclusive@phi)).real/m)
            R = offsum(G)/(m*(m-1))
            check('S20', f'{m}_{c}_ordered_sum', abs(R-c))
            check('S20', f'{m}_{c}_USD_equality', abs(C-(1-R)))
            check('S20', f'{m}_{c}_POVM', max(0., -np.linalg.eigvalsh(fail).min()))
            prior = rng.dirichlet(np.ones(m))
            W = np.sqrt(prior[:,None]*prior[None,:])*G
            bound = 1-offsum(W)/(m-1)
            check('S20', f'{m}_{c}_unequal_prior_feasible', max(0., C-bound))
    # A bound is not an arbitrary-prior optimum: S08 Eq. (10) supplies the actual
    # two-state USD endpoint in this high-bias regime.
    a, b, c = .99, .01, .5
    examples['S20_not_universally_tight'] = {
        'priors':[a,b], 'overlap':c,
        'S20_upper':1-2*math.sqrt(a*b)*c,
        'binary_USD_optimum_from_S08_Eq10':a*(1-c*c)}

    # S22 (Bagan et al. 2017/2018), Lemma 1 / Eq. (9), is the no-failure core.
    for m in (2, 3, 4, 8):
        for c in (.01, .2, .5, .9):
            G = (1-c)*np.eye(m)+c*np.ones((m,m))
            B = psdroot(G)
            C = float(np.sum(abs(np.diag(B))**2)/m)
            E = 1-C
            X = offsum(G)/(m*m)
            predecessor = ((m-2)*E+2*math.sqrt((m-1)*C*E))/m
            current = (m-2)*E/(m-1)+2*math.sqrt(C*E/(m-1))
            check('S22_no_failure', f'{m}_{c}_known_lemma_equality', abs(X-predecessor))
            check('S22_no_failure', f'{m}_{c}_normalization', abs(m*X/(m-1)-current))
            check('S22_no_failure', f'{m}_{c}_upper_root', abs(C-upper(m,c,E)))
        grid = np.linspace(1/m, 1, 401)
        check('S22_no_failure', f'{m}_monotone_physical_branch', max(0., np.max(np.diff([h(m,p) for p in grid]))))

    # Lift S22 through the standard conclusive filter (S08), including changed priors.
    filter_examples = []
    def filtered_case(name, phi, K, measurement_vectors):
        m = phi.shape[1]
        u = K@phi
        omega = K.conj().T@K
        failure = np.eye(phi.shape[0])-omega
        G = phi.conj().T@phi
        A = measurement_vectors.conj().T@u
        q = np.sum(abs(u)**2,axis=0).real
        t = float(q.mean()); F=1-t
        C=float(np.sum(abs(np.diag(A))**2)/m)
        E=max(0.,t-C)
        R=offsum(G)/(m*(m-1))
        check('filtered_lift',name+'_valid_filter',max(0.,-np.linalg.eigvalsh(failure).min()))
        check('filtered_lift',name+'_normalization',abs(C+E+F-1))
        if t < 1e-14:
            check('filtered_lift',name+'_all_failure',abs(C)+abs(E))
            return
        priors=q/(m*t)
        L=offsum(u.conj().T@u)/(m*t)
        cactual=C/t
        fgram=phi.conj().T@failure@phi
        check('filtered_lift',name+'_failure_overlap',max(0.,offsum(fgram)/(m*(m-1))-F))
        check('filtered_lift',name+'_overlap_decomposition',max(0.,R-F-t*L/(m-1)))
        if cactual >= 1/m-1e-12:
            check('filtered_lift',name+'_weighted_lemma',max(0.,L-h(m,cactual)))
            lift=F+t*h(m,cactual)/(m-1)
            direct=F+(m-2)*E/(m-1)+2*math.sqrt(C*E/(m-1))
            check('filtered_lift',name+'_homogeneous_identity',abs(lift-direct))
        else:
            # The upper-root bound is already trivial on this bad-decoder branch;
            # do not use monotonicity of h outside its justified interval.
            check('filtered_lift',name+'_bad_decoder_trivial',max(0.,C-E/(m-1)))
        check('filtered_lift',name+'_complete_upper_root',max(0.,C-upper(m,R,E)))
        if name in ('nonuniform_conditionals','zero_conditional_prior','deliberately_wrong'):
            filter_examples.append(dict(case=name,C=C,E=E,F=F,R=R,conditional_priors=priors.tolist(),conditional_success=cactual))
        return priors
    for m in (2,3,4,8):
        for k in range(8):
            c=rng.uniform(.03,.9)
            G=(1-c)*np.eye(m)+c*np.ones((m,m))
            common=unitary(rng,m)
            phi=common@psdroot(G)
            basis=unitary(rng,m)
            K=(basis*rng.uniform(.05,.95,m))@basis.conj().T
            a,s,b=np.linalg.svd(K@phi)
            meas=a@b
            filtered_case(f'random_{m}_{k}',phi,K,meas)
    prior=filtered_case('nonuniform_conditionals',np.eye(4),np.diag([.2,.4,.7,.9]),np.eye(4))
    check('filtered_lift','nonuniform_conditionals_not_uniform',max(0.,.4-float(prior.max()-prior.min())))
    filtered_case('zero_conditional_prior',np.eye(4),np.diag([0.,.4,.7,.9]),np.eye(4))
    filtered_case('deliberately_wrong',np.eye(4),.7*np.eye(4),np.roll(np.eye(4),1,axis=1))
    filtered_case('all_failure',np.eye(4),np.zeros((4,4)),np.eye(4))
    examples['conditional_filters']=filter_examples

    # Nonzero failure equality witnesses independently reconstruct the achievable
    # constant-overlap alphabet/POVM, not an assumption that a bound is tight for all maps.
    for m in (2,3,4,8):
        for c in (.05,.4,.85):
            G=(1-c)*np.eye(m)+c*np.ones((m,m)); phi=psdroot(G)
            Cme=(math.sqrt(1+(m-1)*c)+(m-1)*math.sqrt(1-c))**2/m**2
            for fraction in (0.,.25,.75,1.):
                E=fraction*(1-Cme)
                C=upper(m,c,E)
                B=np.full((m,m),math.sqrt(E/(m-1)))
                np.fill_diagonal(B,math.sqrt(C))
                M=B@np.linalg.inv(phi)
                failure=np.eye(m)-M.conj().T@M
                F=float(np.trace(phi.conj().T@failure@phi).real/m)
                rhs=F+(m-2)*E/(m-1)+2*math.sqrt(C*E/(m-1))
                check('finite_failure_attainment',f'{m}_{c}_{fraction}_feasible',max(0.,-np.linalg.eigvalsh(failure).min()))
                check('finite_failure_attainment',f'{m}_{c}_{fraction}_normalization',abs(C+E+F-1))
                check('finite_failure_attainment',f'{m}_{c}_{fraction}_equality',abs(rhs-c))

    # Optical all-intensity composition: finite examples check factors/directions.
    # Jensen's analytic argument, not these samples, handles unbounded support.
    schemes=[([.5,.5],[0.,2.]),([.999,.001],[0.,500.]),([.99,.01],[.1,50.])]
    for m in (2,4,5):
        maps=[]
        for j in range(m):
            A=rng.normal(size=(3,3))+1j*rng.normal(size=(3,3))
            maps.append(.85*A/np.linalg.norm(A,2))
        H=sum((maps[j]-maps[k]).conj().T@(maps[j]-maps[k]) for j in range(m) for k in range(j+1,m))/(m*(m-1))
        kap=float(np.linalg.eigvalsh(H)[-1])
        for case,(weights,energies) in enumerate(schemes):
            totals=np.zeros(3); ratios=[]
            for weight,N in zip(weights,energies):
                direction=rng.normal(size=3)+1j*rng.normal(size=3)
                alpha=math.sqrt(N)*direction/np.linalg.norm(direction)
                betas=np.array([A@alpha for A in maps])
                norms=np.sum(abs(betas)**2,axis=1)
                Gram=np.exp(-.5*(norms[:,None]+norms[None,:])+betas.conj()@betas.T)
                R=offsum(Gram)/(m*(m-1))
                check('optical_composition',f'{m}_{case}_{N}_coherent_overlap',max(0.,math.exp(-kap*N)-R))
                amplitudes=psdroot(Gram)
                accept=.8
                C=accept*float(np.sum(abs(np.diag(amplitudes))**2)/m)
                E=accept-C
                F=1-accept
                check('optical_composition',f'{m}_{case}_{N}_single_pulse_bound',max(0.,C-upper(m,math.exp(-kap*N),E)))
                totals+=weight*np.array([C,E,F])
                ratios.append(R)
            C,E,F=totals; mean=float(np.dot(weights,energies))
            Rmix=float(np.dot(weights,ratios))
            check('optical_composition',f'{m}_{case}_mixture_overlap',max(0.,math.exp(-kap*mean)-Rmix))
            check('optical_composition',f'{m}_{case}_mixture_score',max(0.,C-upper(m,math.exp(-kap*mean),E)))
            if m==4 and case==1:
                examples['rare_bright_finite_example']=dict(weights=weights,energies=energies,mean=mean,kappa=kap,C=float(C),E=float(E),classical_C_upper=upper(m,math.exp(-kap*mean),E))

    # S18: supports of distinct pure outputs, not a new bosonic discrimination theorem.
    regularized=[]
    for x in (.01,.7,1.,5.):
        c=math.exp(-x)
        a=np.array([1.,0.]); b=np.array([c,math.sqrt(1-c*c)])
        rho=np.outer(a,a); sigma=np.outer(b,b)
        outside=float(np.trace(rho@(np.eye(2)-sigma)))
        check('S18_scope',f'{x}_support_weight',abs(outside-(1-c*c)))
        vals=[]
        for epsilon in (1e-3,1e-6,1e-9):
            e,V=np.linalg.eigh((1-epsilon)*sigma+epsilon*np.eye(2)/2)
            d=-float(np.trace(rho@(V*np.log(e))@V.T))
            vals.append(d)
        check('S18_scope',f'{x}_regularized_divergence_increases',max(0.,-min(np.diff(vals))))
        regularized.append(dict(t_mu=x,overlap=c,outside_support=outside,regularized_relative_entropies=vals))
    examples['S18_pure_output_support']=regularized
    # A diagonal signal marginal need not mean the entire probe is incoherent.
    states=[]
    for gamma in (.1,.4):
        rho=np.zeros((4,4));rho[0,0]=rho[3,3]=.5
        rho[0,3]=rho[3,0]=.5*math.exp(-gamma/2)
        states.append(rho)
    difference=states[0]-states[1]
    trace_distance=.5*float(np.sum(abs(np.linalg.eigvalsh(difference))))
    check('S18_scope','purification_not_signal_marginal',abs(trace_distance-.5*abs(math.exp(-.05)-math.exp(-.2))))
    check('S18_scope','signal_marginal_difference',abs(np.trace(difference[:2,:2]))+abs(np.trace(difference[2:,2:])) )
    examples['S18_reference_distinction']=dict(signal_marginal_difference=0.,joint_trace_distance=trace_distance)

    result=dict(status='PASS',seed=SEED,baseline=BASELINE,checks=len(checks),
        groups=dict(Counter(c['group'] for c in checks)),max_residual=max(c['residual'] for c in checks),
        declared_tolerance=TOL,script_sha256=script_hash,ledger=checks,examples=examples,
        scope='Finite predecessor-normalization, conclusive-filter and optical-composition checks. Universal reasoning is in REDUCTIONS.md. No originality or experimental certificate.',
        canonical_code_imported=False,canonical_files_written=False,external_article_code_used=False,lab_data_used=False)
    env=dict(python=sys.version,numpy=np.__version__,platform=platform.platform(),
        source_model='Independent formulas; no canonical module imported and no authenticated local Git checkout claimed.',network_used_by_script=False)
    out.mkdir(parents=True)
    (out/'RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    (out/'ENVIRONMENT.json').write_text(json.dumps(env,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('status','checks','groups','max_residual','examples')},indent=2))

if __name__=='__main__':
    main()
