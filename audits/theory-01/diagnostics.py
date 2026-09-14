"""Independent, bounded audit diagnostics for the pinned optical-reading baseline.

No network, no laboratory data, and no changes to the reference files. Universal
claims are addressed in INDEPENDENT_DERIVATIONS.md. This script checks explicit
instances and produces numerical certificates, not formal or interval proofs.
Run: python audits/theory-01/diagnostics.py --root . --output /new/directory
"""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
import math
import platform
import sys
import time
from pathlib import Path
import importlib.util
import numpy as np
import scipy
from scipy.optimize import linprog
import mpmath as mp

SEED = 202609140101
RNG = np.random.default_rng(SEED)
LEDGER = []
TABLES = {}


def check(name, value, tolerance=1e-9):
    value = float(value)
    if not math.isfinite(value) or value < 0 or value > tolerance:
        raise AssertionError(f'{name}: {value} not in [0,{tolerance}]')
    LEDGER.append(dict(name=name,residual=value,tolerance=tolerance))


def require(name, condition):
    check(name, 0.0 if condition else 1.0, 0.0)


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    obj = importlib.util.module_from_spec(spec)
    sys.modules[name] = obj
    spec.loader.exec_module(obj)
    return obj


def herm(a):
    return (a+a.conj().T)/2


def rootpsd(a):
    w,u=np.linalg.eigh(herm(a))
    return (u*np.sqrt(np.maximum(w,0)))@u.conj().T


def fourier(m):
    return np.exp(2j*np.pi*np.outer(np.arange(m),np.arange(m))/m)


def independent_probe(eta,lam):
    """80-digit scalar bisection, not the reference double-precision eigensolver."""
    m=len(eta);l=max(lam,1/(m-1))
    with mp.workdps(80):
        e=[mp.mpf(str(v)) for v in eta];L=mp.mpf(str(l))
        lo=mp.mpf(0);hi=max(e)
        for _ in range(280):
            b=(lo+hi)/2
            f=(1+L)/m*sum(x/(b+L*x) for x in e)-1
            if f>0:lo=b
            else:hi=b
        b=(lo+hi)/2
        p=[x/(b+L*x)**2 for x in e];norm=sum(p)
        p=[float(x/norm) for x in p]
        beta=float(b)
    return beta,np.array(p)


def states_photon(eta,p,Z):
    m=len(eta);states=[]
    for j in range(m):
        v=np.sqrt(eta*p)*Z[:,j]
        rho=np.zeros((m+1,m+1),complex)
        rho[:m,:m]=np.outer(v,v.conj())
        rho[m,m]=1-np.dot(eta,p)
        states.append(rho)
    return np.array(states)


def rates(states,effects):
    m=len(states)
    raw=np.real(np.einsum('aij,bji->ab',states,effects))
    C=float(np.trace(raw)/m);con=float(raw.sum()/m)
    return C,con-C,1-con


def code_measurement(Z,guess_vacuum=False):
    m=len(Z);effects=[]
    for j in range(m):
        v=np.r_[Z[:,j]/np.sqrt(m),0]
        M=np.outer(v,v.conj())
        if guess_vacuum:M[-1,-1]=1/m
        effects.append(M)
    return np.array(effects)


def generic_povm(d,n):
    blocks=[RNG.normal(size=(d,d))+1j*RNG.normal(size=(d,d)) for _ in range(n+1)]
    pos=[b@b.conj().T for b in blocks]
    w,u=np.linalg.eigh(sum(pos));inv=(u*(1/np.sqrt(w)))@u.conj().T
    return np.array([inv@p@inv for p in pos[:-1]])


def hermitian_basis(d):
    B=[]
    for i in range(d):
        M=np.zeros((d,d),complex);M[i,i]=1;B.append(M)
    for i in range(d):
        for j in range(i):
            M=np.zeros((d,d),complex);M[i,j]=M[j,i]=1;B.append(M)
            M=np.zeros((d,d),complex);M[i,j]=1j;M[j,i]=-1j;B.append(M)
    return np.array(B)


def dual_cuts(states,lam,limit=900):
    """Full Hermitian discrimination dual via spectral cuts and LP.

    Minimize tr Y subject to Y >= payoff_j and Y >= 0. No diagonal
    restriction, no imported reference objective, and no dedicated SDP solver.
    Returned Y is shifted to satisfy every full-matrix constraint numerically.
    The shift, minimum eigenvalue and gap are retained, rather than treating an
    incomplete cutting-plane relaxation as a valid upper certificate.
    """
    m,d,_=states.shape;B=hermitian_basis(d)
    pay=(1+lam)*states/m-lam*states.mean(axis=0)
    A=np.concatenate((pay,np.zeros((1,d,d),complex)))
    rows=[];rhs=[]
    def add(v):
        rows.append(-np.real(np.einsum('i,kij,j->k',v.conj(),B,v)))
        rhs.append(-max(float(np.vdot(v,a@v).real) for a in A))
    for i in range(d):add(np.eye(d)[:,i])
    for i in range(d):
        for j in range(i):
            for phase in (1,-1,1j,-1j):
                v=np.zeros(d,complex);v[i]=1/np.sqrt(2);v[j]=phase/np.sqrt(2);add(v)
    obj=np.trace(B,axis1=1,axis2=2).real
    last_sol=None;lp_note='converged'
    for step in range(limit):
        sol=linprog(obj,A_ub=np.array(rows),b_ub=np.array(rhs),bounds=[(None,None)]*len(B),method='highs',
            options={'primal_feasibility_tolerance':1e-9,'dual_feasibility_tolerance':1e-9})
        if not sol.success:
            sol=linprog(obj,A_ub=np.array(rows),b_ub=np.array(rhs),bounds=[(None,None)]*len(B),method='highs-ipm',
                options={'presolve':False,'primal_feasibility_tolerance':1e-8,'dual_feasibility_tolerance':1e-8})
        if not sol.success:
            if last_sol is None:raise RuntimeError(sol.message)
            lp_note='LP stopped; repaired previous feasible-constraint iterate: '+sol.message
            sol=last_sol
            break
        last_sol=sol
        Y=np.einsum('k,kij->ij',sol.x,B)
        worst=0
        for a in A:
            w,u=np.linalg.eigh(herm(Y-a));worst=max(worst,float(-w[0]))
            if w[0]<-5e-9:add(u[:,0])
        if worst<=5e-9:break
    bump=max(worst,0)+1e-10
    Y=Y+bump*np.eye(d)
    min_eig=min(float(np.linalg.eigvalsh(herm(Y-a))[0]) for a in A)
    return dict(matrix=Y,upper=float(np.trace(Y).real),lp_lower=float(sol.fun),
                repair=bump,minimum_eigenvalue=min_eig,iterations=step+1,cut_count=len(rows),lp_note=lp_note)


def audit_photon(ref):
    records=[];dual_records=[]
    for m in (2,3,4,5,8):
        Z=fourier(m)
        for k in range(3):
            eta=np.exp(RNG.uniform(np.log(.035),0,m))
            for lam in (0.,1/(m-1),1.,5.,60.):
                beta,p=independent_probe(eta,lam)
                states=states_photon(eta,p,Z)
                M=code_measurement(Z,lam<1/(m-1))
                C,E,F=rates(states,M)
                answer=ref.photon_score(eta,lam)
                check(f'photon_rates_{m}_{k}_{lam}',max(abs(C-answer['C']),abs(E-answer['E']),abs(F-answer['F'])),2e-10)
                check(f'photon_input_{m}_{k}_{lam}',np.max(abs(p-answer['p'])),2e-10)
                if lam>=1/(m-1):check(f'photon_dual_value_{m}_{k}_{lam}',abs(C-lam*E-beta),1e-10)
                for trial in range(2):
                    q=RNG.dirichlet(np.ones(m));rhos=states_photon(eta,q,Z)
                    c,e,_=rates(rhos,generic_povm(m+1,m))
                    check(f'photon_arbitrary_measurement_{m}_{k}_{lam}_{trial}',max(0,c-lam*e-answer['score']))
                records.append(dict(m=m,eta=eta.tolist(),penalty=lam,C=C,E=E,F=F,p=p.tolist()))
                if m in (3,4) and k==0 and lam in (0.,5.):
                    print('  photon dual',m,lam,flush=True)
                    cert=dual_cuts(states[:,:m,:m],lam)
                    vacuum_payoff=max(0.,float(np.max((1+lam)*states[:,-1,-1].real/m-lam*states[:,-1,-1].real.mean())))
                    cert['upper']+=vacuum_payoff
                    cert['vacuum_payoff']=vacuum_payoff
                    cert['matrix_scope']='Full Hermitian photon block; input states are block diagonal in photon/vacuum, so pinching is lossless.'
                    gap=cert['upper']-(C-lam*E)
                    check(f'full_hermitian_dual_gap_{m}_{lam}',abs(gap),3e-6)
                    check(f'full_hermitian_dual_psd_{m}_{lam}',max(0,-cert['minimum_eigenvalue']),1e-10)
                    cert.update(m=m,penalty=lam,primal=C-lam*E,gap=gap,eta=eta,p=p)
                    dual_records.append(cert)
            edge=ref.photon_score(eta,1/(m-1))
            E0=edge['E'];F0=edge['F'];Pme=edge['C']+F0/m
            for eps in (0.,.2*E0,.8*E0,E0+.4*F0*(m-1)/m,1-Pme,1.):
                r=ref.photon_frontier(eta,eps);states=states_photon(eta,np.array(r['p']),Z)
                M=code_measurement(Z,False)
                surv=eta@r['p'];vac=1-surv
                c0,e0,_=rates(states,M)
                fraction=0 if vac<1e-14 else (r['E']-e0)/(vac*(m-1)/m)
                fraction=float(np.clip(fraction,0,1));M[:,-1,-1]=fraction/m
                c,e,f=rates(states,M)
                check(f'frontier_achievability_{m}_{k}_{eps}',max(abs(c-r['C']),abs(e-r['E']),abs(f-r['F'])),1e-8)
                check(f'frontier_budget_{m}_{k}_{eps}',max(0,e-eps),1e-8)
    TABLES['photon']=records;TABLES['dual_certificates']=dual_records


def coherent_gram(outputs):
    norms=np.sum(abs(outputs)**2,axis=1)
    return np.exp(-.5*(norms[:,None]+norms[None,:])+outputs.conj()@outputs.T)


def contrast(maps):
    m=len(maps);center=maps.mean(axis=0)
    return sum((a-center).conj().T@(a-center) for a in maps)/(m-1)


def state_columns(G):
    return rootpsd(G)


def pure_density(columns):
    return np.array([np.outer(v,v.conj()) for v in columns.T])


def audit_classical(ref):
    records=[]
    for x in (0.,1e-7,.07,.7,2.,8.):
        A=-np.expm1(-x);c=1-A;G=A*np.eye(4)+c*np.ones((4,4))
        J=np.ones((4,4))/4
        Phi=np.sqrt(A)*(np.eye(4)-J)+np.sqrt(1+3*c)*J
        if x==0:
            for eps in (0.,.15,.75,.95):
                z=ref.classical_uniform_frontier(x,eps)
                check(f'zero_energy_guess_{eps}',abs(z['C']-min(.25,eps/3)))
            continue
        Pme=np.trace(Phi).real**2/16;Eme=1-Pme
        for f in (0.,.1,.5,1.):
            E=f*Eme;C=(np.sqrt(-np.expm1(-x))+np.sqrt(E/3))**2
            B=np.full((4,4),np.sqrt(E/3));np.fill_diagonal(B,np.sqrt(C))
            # Solve the amplitude equation independently; no reference POVM builder.
            T=np.linalg.solve(Phi.T,B.T).T
            failure=herm(np.eye(4)-T.conj().T@T)
            M=np.array([np.outer(r.conj(),r) for r in T])
            cc,ee,ff=rates(pure_density(Phi),M)
            check(f'classical_povm_psd_{x}_{f}',max(0,-np.linalg.eigvalsh(failure)[0]),5e-9)
            check(f'classical_povm_rates_{x}_{f}',max(abs(C-cc),abs(E-ee),abs(1-C-E-ff)),2e-9)
            r=ref.classical_uniform_frontier(x,E)
            check(f'classical_frontier_reference_{x}_{f}',abs(r['C']-cc),2e-9)
            records.append(dict(x=x,fraction=f,C=cc,E=ee,F=ff,min_failure_eigenvalue=float(np.linalg.eigvalsh(failure)[0])))
        if x in (.07,.7,2.):
            lam=5.;E=min(Eme,(1-c)/(3*(lam-1/3)**2));C=(np.sqrt(1-c)+np.sqrt(E/3))**2
            print('  classical dual',x,lam,flush=True)
            cert=dual_cuts(pure_density(Phi),lam)
            gap=cert['upper']-(C-lam*E)
            check(f'classical_full_dual_{x}',abs(gap),3e-6)
            cert.update(kind='classical',x=x,penalty=lam,primal=C-lam*E,gap=gap)
            TABLES['dual_certificates'].append(cert)
    TABLES['classical_uniform']=records
    # Independent complete complex coherent-state Gram matrices, random physical
    # contractions and arbitrary finite POVMs, including preparation-label mixtures.
    mix=[]
    for m in (2,3,4,6):
        maps=[]
        for _ in range(m):
            a=RNG.normal(size=(3,2))+1j*RNG.normal(size=(3,2));a/=np.linalg.norm(a,2)*1.2;maps.append(a)
        maps=np.array(maps);H=contrast(maps);k=float(np.linalg.eigvalsh(H)[-1])
        hh,kk=ref.contrast_operator(maps)
        check(f'contrast_center_identity_{m}',np.linalg.norm(H-hh),1e-12)
        vals=[]
        for pulse,N in enumerate((0.,.01,.1,1.,10.,100.)):
            direction=RNG.normal(size=2)+1j*RNG.normal(size=2);direction/=np.linalg.norm(direction)
            outputs=np.einsum('mij,j->mi',maps,np.sqrt(N)*direction)
            G=coherent_gram(outputs)
            Phi=np.ones((m,m))/np.sqrt(m) if N==0 else rootpsd(G)
            rhos=pure_density(Phi)
            C,E,F=rates(rhos,generic_povm(m,m))
            ov=sum(abs(G[j,l]) for j in range(m) for l in range(j))*2/(m*(m-1))
            measured=F+2*np.sqrt(C*E/(m-1))+(m-2)*E/(m-1)
            check(f'coherent_overlap_input_{m}_{pulse}',max(0,np.exp(-k*N)-ov))
            check(f'coherent_overlap_output_{m}_{pulse}',max(0,ov-measured))
            check(f'classical_rate_bound_{m}_{pulse}',max(0,C-ref.classical_correct_upper(k,N,E,m)))
            vals.append((N,C,E))
        weights=RNG.dirichlet(np.ones(len(vals)));N,C,E=weights@np.array(vals)
        check(f'labelled_mixture_{m}',max(0,C-ref.classical_correct_upper(k,N,E,m)))
        mix.append(dict(m=m,energy=N,C=C,E=E,kappa=k))
    # Flash pulses with unboundedly increasing energy, under a fixed mean.
    for peak in (1.,10.,1e3,1e8,1e16):
        for lam in (.4,1.,5.):
            weight=1/peak
            C=weight*(-np.expm1(-peak));E=0.
            upper=ref.classical_score_upper(1.,1.,lam)
            check(f'flash_no_peak_{peak}_{lam}',max(0,C-lam*E-upper))
            b,nu=ref.affine_classical_witness(1.,1.,lam)
            check(f'flash_support_{peak}_{lam}',max(0,-np.expm1(-peak)-b-nu*peak),1e-7)
    TABLES['classical_mixture']=mix


def audit_maps_and_reverse(ref):
    rows=[]
    for trial in range(30):
        m=4;d=4
        base=[];actual=[];radii=[]
        for _ in range(m):
            a=RNG.normal(size=(d,d))+1j*RNG.normal(size=(d,d));a*=.65/np.linalg.norm(a,2)
            change=RNG.normal(size=(d,d))+1j*RNG.normal(size=(d,d));change*=.03/np.linalg.norm(change,2)
            base.append(a);actual.append(a+change);radii.append(np.linalg.norm(change,2))
        base=np.array(base);actual=np.array(actual)
        khat=np.linalg.eigvalsh(contrast(base))[-1];k=np.linalg.eigvalsh(contrast(actual))[-1]
        bound=ref.robust_contrast_upper(khat,radii)
        check(f'map_radius_{trial}',max(0,k-bound))
        psi=RNG.normal(size=d)+1j*RNG.normal(size=d);psi/=np.linalg.norm(psi)
        distances=[]
        for j in range(m):
            def state(a):
                v=a@psi;rho=np.zeros((d+1,d+1),complex);rho[:d,:d]=np.outer(v,v.conj());rho[-1,-1]=1-np.vdot(v,v).real;return rho
            x=state(actual[j]);y=state(base[j]);distance=np.linalg.norm(x-y,ord='nuc')/2
            check(f'reverse_trace_bound_{trial}_{j}',max(0,distance-2*radii[j]),1e-12)
            distances.append(distance)
        rows.append(dict(kappa=k,kappa_upper=bound,max_trace_distance=max(distances)))
    Z=np.ones((4,4))-2*np.eye(4);maps=np.array([np.diag(Z[:,j]) for j in range(4)],complex)
    phased=maps.copy();phased[0]*=-1
    check('global_phase_contrast_1',abs(np.linalg.eigvalsh(contrast(maps))[-1]-1),1e-12)
    check('global_phase_contrast_4over3',abs(np.linalg.eigvalsh(contrast(phased))[-1]-4/3),1e-12)
    for _ in range(25):
        eta=RNG.uniform(.01,.9,4);up=eta+RNG.random(4)*(1-eta)
        for lam in (.1,5.):
            check(f'transmission_monotonicity_{len(LEDGER)}',max(0,ref.photon_score(eta,lam)['score']-ref.photon_score(up,lam)['score']))
    TABLES['map_robustness']=rows


def score_tail(n,lam,C,E,threshold):
    # Exact finite convolution on integer score values {-lam,0,1}.
    q=np.zeros(lam+2);q[0]=E;q[lam]=1-C-E;q[lam+1]=C
    dist=np.array([1.])
    for _ in range(n):dist=np.convolve(dist,q)
    scores=np.arange(len(dist))-lam*n
    return float(dist[scores>n*threshold+1e-11].sum())


def audit_statistics(ref):
    rows=[]
    for lam in (1,5):
        for n in (100,400):
            alpha=.05;U=.12
            radius=ref.fixed_n_radius(n,lam,alpha)
            max_tail=0
            for E in np.linspace(0,(1-U)/(lam+1),13):
                C=U+lam*E;tail=score_tail(n,lam,C,float(E),U+radius)
                max_tail=max(max_tail,tail)
                check(f'exact_fixedN_tail_{lam}_{n}_{E}',max(0,tail-alpha),2e-12)
            rows.append(dict(n=n,penalty=lam,alpha=alpha,upper=U,radius=radius,largest_exact_tail=max_tail))
    # Negative control: a mean budget only across whole runs is not a predictable
    # conditional budget. This is EXCLUDED by the actual theorem.
    n=1000;lam=5;alpha=.01;peak=10.;q=1-np.exp(-peak)
    threshold=ref.classical_score_upper(1,1,lam)+ref.fixed_n_radius(n,lam,alpha)
    lower=.1*q**n
    require('excluded_run_level_mixture_is_counterexample',threshold<1 and lower>alpha)
    TABLES['statistics']=rows
    TABLES['excluded_access_negative_control']=dict(N=n,rare_run_probability=.1,bright_mean=peak,
          across_runs_mean=1.,claimed_alpha_if_misapplied=alpha,rejection_probability_lower_bound=lower,
          threshold_if_misapplied=threshold,violates_theorem=False,
          reason='Run-shared latent brightness violates the iid/predictable-budget assumptions.')


def direct_mask_law(eta,p,pn,eff,dark,sigma,order=7):
    """Independent quadrature + multinomial + dark-mask enumeration.
    Unlike reference Fourier-polynomial/no-click inclusion-exclusion code.
    """
    Z=np.ones((4,4))-2*np.eye(4);D=Z/2
    h,w=np.polynomial.hermite.hermgauss(order);w/=np.sqrt(np.pi)
    grid=np.array(list(itertools.product(range(order),repeat=4)))
    phases=np.sqrt(2)*sigma*h[grid];weights=np.prod(w[grid],axis=1)
    dark_law=np.array([np.prod([dark[k] if mask>>k&1 else 1-dark[k] for k in range(4)]) for mask in range(16)])
    P=np.zeros((4,16))
    for j in range(4):
        phi=np.sqrt(eta*p)[None,:]*Z[:,j][None,:]*np.exp(1j*phases)
        wdet=abs(phi@D.T)**2*eff
        probs=np.c_[1-wdet.sum(axis=1),wdet]
        base=np.zeros(16)
        for n,mass in enumerate(pn):
            for occ in itertools.product(range(n+1),repeat=5):
                if sum(occ)!=n:continue
                occ=np.array(occ);coeff=math.factorial(n)/math.prod(math.factorial(int(x)) for x in occ)
                likelihood=np.prod(probs**occ,axis=1)
                mask=sum((1<<k) for k in range(4) if occ[k+1])
                base[mask]+=mass*coeff*np.dot(weights,likelihood)
        for a,b in itertools.product(range(16),repeat=2):P[j,a|b]+=base[a]*dark_law[b]
    return P


def audit_readout(root,ref,optics,analyzer):
    eta=np.array([.7,.5,.9,.35]);p=np.array([.1,.2,.3,.4]);pn=np.array([.11,.78,.09,.02])
    eff=np.array([.83,.91,.75,.88]);dark=np.array([.001,.003,.0005,.002]);sigma=.065
    P=direct_mask_law(eta,p,pn,eff,dark,sigma)
    old=optics.source_click_probabilities(eta,p,pn,eff,dark,sigma)
    check('independent_quadrature_multinomial_clicks',np.max(abs(P-old)),2e-10)
    check('all_masks_normalize',np.max(abs(P.sum(axis=1)-1)),2e-12)
    plan=json.loads((root/'templates/primary_plan.example.json').read_text());plan['fixed_N']=64
    rows=[]
    for j in range(4):
        for mask in range(16):
            rows.append(dict(trial_id=str(len(rows)),condition_id=plan['condition_id'],calibration_id=plan['calibration_id'],
                phase_code_id=plan['phase_code_id'],receiver_id=plan['receiver_id'],hidden_label=str(j),click_mask=str(mask)))
    out=analyzer.analyze(plan,rows,True)
    require('all_16_masks_accounted',out['counts']==dict(correct=4,wrong=12,inconclusive=48))
    for label,mutate in [
        ('duplicate_id',lambda p,r:r[1].update(trial_id=r[0]['trial_id'])),
        ('bad_calibration',lambda p,r:r[0].update(calibration_id='wrong')),
        ('missing_trial',lambda p,r:r.pop()),
        ('bad_label',lambda p,r:r[0].update(hidden_label='4')),
        ('bad_mask',lambda p,r:r[0].update(click_mask='16')),
        ('nonfinite_budget',lambda p,r:p.update(mean_energy_upper=float('nan'))),
        ('bad_alpha',lambda p,r:p.update(alpha_stat=0)),
        ('unapproved_real_plan',lambda p,r:p.update(synthetic=False))]:
        pp=plan.copy();rr=[v.copy() for v in rows];mutate(pp,rr)
        try:analyzer.analyze(pp,rr,True)
        except (ValueError,KeyError):rejected=True
        else:rejected=False
        require('reject_'+label,rejected)
    # Recompute both published synthetic cases independently from counts/radii.
    for name in ('synthetic_certification_example.json','synthetic_reverse_example.json'):
        a=json.loads((root/'results'/name).read_text())
        n=a['N'];counts=a['counts'];score=(counts['correct']-5*counts['wrong'])/n
        radius=6*np.sqrt(np.log(4000)/(2*n));upper=a.get('classical_upper',a.get('one_photon_upper'))
        subtraction=a.get('multiphoton_tail_subtraction',0)
        expected=score-radius-upper-subtraction
        check('recompute_'+name,abs(expected-a['certified_gap']),1e-12)
    TABLES['independent_detector_matrix']=P
    TABLES['mask_accounting']=out['counts']


def audit_findings(ref):
    # Reproduce defects without modifying canonical source or widening claims.
    lam=5.;x=3.;K=15/14
    raw=K*(1-np.exp(-x));capped=ref.classical_score_upper(1,x,lam)
    require('F01_false_printed_uncapped_chain',raw>1 and capped==1)
    eta=np.array([.2,.4,.8,.9]);L=1e15
    actual=ref.photon_score(eta,L)
    mpbeta,_=independent_probe(eta,L);H=4/np.sum(1/eta)
    stress=[]
    for penalty in (1e12,1e14,1e15,1e16,1e17,1e18):
        val=ref.photon_score(eta,penalty)['score'];truth,_=independent_probe(eta,penalty)
        stress.append(dict(penalty=penalty,computed_score=val,independent_score=truth))
    require('F02_large_penalty_loss_of_accuracy',any(abs(r['computed_score']-r['independent_score'])>.01 for r in stress))
    TABLES['findings']=[
        dict(id='F01',kind='proof transcription',location='proofs/THEORY.md section 4',
             printed_claim='S <= K*(1-exp(-kappa*mu)) <= 1',raw_value=raw,code_value=capped,
             correct_form='S <= min(1,K*(1-exp(-kappa*mu)))',affects_lambda5_primary=False),
        dict(id='F02',kind='numerical domain',location='src/theory.py photon_score',
             eta=eta,penalty=L,computed_score=actual['score'],computed_C=actual['C'],computed_E=actual['E'],
             eigenvalue=actual['eigenvalue'],independent_80_digit_score=mpbeta,zero_error_feasible_score=H,
             reason='Cancellation in C-lambda*E can yield an invalid theoretical upper value at large accepted finite penalties.',
             affects_lambda5_primary=False,stress_cases=stress),
        dict(id='F03',kind='terminology',location='src/theory.py classical_uniform_frontier docstring',
             text='Includes positive-P mixtures',
             reason='The proof correctly requires a nonnegative Glauber-Sudarshan distribution, not the doubled positive-P representation.',
             affects_numerical_result=False)]


def serialize(x):
    if isinstance(x,np.ndarray):
        if np.iscomplexobj(x):return dict(real=x.real.tolist(),imag=x.imag.tolist())
        return x.tolist()
    if isinstance(x,np.generic):return x.item()
    raise TypeError(type(x).__name__)


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args();root=args.root.resolve();out=args.output.resolve()
    if out.exists():ap.error('output must be a new directory')
    if out==root or root/'results'==out or (root/'results' in out.parents):ap.error('use a new audit output directory, not canonical results')
    expected={'src/theory.py':'68e01d4f45b0bdc2dc5f87c1c8c14c9dd54325bafce2d274baac71dd707fa3fe',
              'src/analyze_trials.py':'799f07af67d244eed6c830356101f4d7118cb9d4ceeceed0f61aad7b306b64a9',
              'src/optics.py':'d17a07f3d9de80f1d6e3ba96547b341c084b3caf77fbca0e3480188fc27acdbc'}
    for rel,digest in expected.items():
        if hashlib.sha256((root/rel).read_bytes()).hexdigest()!=digest:raise ValueError('Audit target differs: '+rel)
    out.mkdir(parents=True);start=time.time()
    sys.path.insert(0,str(root/'src'))
    ref=load(root/'src/theory.py','theory');optics=load(root/'src/optics.py','optics');analyzer=load(root/'src/analyze_trials.py','analyze_trials')
    for func in (audit_photon,audit_classical,audit_maps_and_reverse,audit_statistics):
        print(func.__name__,flush=True);func(ref)
    print('audit_readout',flush=True);audit_readout(root,ref,optics,analyzer)
    audit_findings(ref)
    for rel,digest in expected.items():require('unchanged_'+rel,hashlib.sha256((root/rel).read_bytes()).hexdigest()==digest)
    summary=dict(status='PASS_WITH_REPRODUCED_FINDINGS',baseline='d07e4e2180992ab52ee08d0a0cad689154d2e9bd',
      seed=SEED,checks=len(LEDGER),max_residual=max(a['residual'] for a in LEDGER),
      elapsed_seconds=time.time()-start,python=sys.version,numpy=np.__version__,scipy=scipy.__version__,mpmath=mp.__version__,platform=platform.platform(),
      independent_method='Full Hermitian spectral cutting-plane LP dual with explicit PSD repair; 80-digit scalar root; complex Gram/POVM reconstruction; multinomial-quadrature detector enumeration; exact finite score convolution.',
      dedicated_SDP_solver=False,interval_arithmetic=False,formal_proof_assistant=False,lab_data=False,
      source_hashes=expected,scope='Independent bounded scientific/operational audit. No novelty clearance or automatic repair.')
    (out/'SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n')
    (out/'CHECKS.json').write_text(json.dumps(LEDGER,indent=2)+'\n')
    (out/'DIAGNOSTICS.json').write_text(json.dumps(TABLES,indent=2,default=serialize)+'\n')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
