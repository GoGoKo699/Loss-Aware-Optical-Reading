"""Reproduce new results and independent checks. No network calls; no lab data."""
from __future__ import annotations
import csv, hashlib, itertools, json, math, os, platform, sys, time
from pathlib import Path
from decimal import Decimal, localcontext
import numpy as np
import scipy
from scipy.linalg import hadamard, sqrtm, expm
from scipy.optimize import minimize
from theory import *
from optics import *

ROOT=Path(__file__).resolve().parents[1]
# Migration-only I/O guard: mathematical validation below is unchanged.
import argparse
_output_parser = argparse.ArgumentParser(description=__doc__)
_output_parser.add_argument('--output-dir', required=True,
    help='New directory outside frozen results; never overwrites an existing run.')
OUT=Path(_output_parser.parse_args().output_dir).resolve()
_frozen=(ROOT/'results').resolve()
_runs=(_frozen/'runs').resolve()
if (OUT == _frozen or OUT == _runs or
    (_frozen in OUT.parents and _runs not in OUT.parents)):
    _output_parser.error('Use a new results/runs/<name> directory, not archived results.')
OUT.mkdir(parents=True, exist_ok=False)
RNG=np.random.default_rng(2026091417);START=time.perf_counter();CHECKS=[]

def check(name,residual,tol=3e-10):
    r=float(abs(residual));CHECKS.append({'name':name,'residual':r,'tolerance':tol})
    if not np.isfinite(r) or r>tol:raise AssertionError(f'{name}: {r} > {tol}')

def savecsv(name,rows):
    with (OUT/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def jsonsave(name,x):
    def default(o):
        if isinstance(o,np.ndarray):return o.tolist()
        if isinstance(o,np.generic):return o.item()
        raise TypeError(type(o).__name__)
    (OUT/name).write_text(json.dumps(x,indent=2,default=default)+'\n')

def roots(G):
    w,U=np.linalg.eigh((G+G.conj().T)/2)
    return (U*np.sqrt(np.maximum(w,0)))@U.conj().T

# 1. Quantum global certificate, direct optical states, and a separate secular solver.
rows=[]
for m in [4,8]:
    S=four_code() if m==4 else hadamard(m).astype(float)
    D=S.conj().T/np.sqrt(m)
    for c in range(24):
        eta=RNG.uniform(.025,1,m)
        for lam in [1/(m-1),1.,5.,40.,2000.]:
            o=photon_score(eta,lam);b,p2=photon_secular(eta,lam)
            check(f'quantum_secular_{m}_{c}_{lam}',max(abs(b-o['score']),np.max(abs(p2-o['p']))),2e-9)
            phi=np.diag(np.sqrt(eta*o['p']))@S
            amp=D@phi;C=np.mean(abs(np.diag(amp))**2);E=np.sum(abs(amp)**2)/m-C
            check(f'direct_achievability_{m}_{c}_{lam}',max(abs(C-o['C']),abs(E-o['E'])))
            # Full discrimination dual for this input, independent of the input upper-bound proof.
            q=eta*o['p'];Y=np.diag(o['score']*o['p'])
            for j in range(m):
                W=(1+lam)*np.outer(phi[:,j],phi[:,j].conj())/m-lam*np.diag(q)
                check(f'dual_psd_{m}_{c}_{lam}_{j}',max(0,-np.linalg.eigvalsh(Y-W)[0]),3e-9)
            check(f'dual_trace_{m}_{c}_{lam}',abs(np.trace(Y)-o['score']))
            if c==0:
                rows.append({'m':m,'penalty':lam,'score':o['score'],'correct':o['C'],'wrong':o['E'], 'inconclusive':o['F']})
savecsv('dimension_transfer.csv',rows)

# 2. Arbitrary POVMs/probes, not merely the proposed decoder. All are feasible lower scores.
for c in range(500):
    m=4 if c%2 else 8;eta=RNG.uniform(.01,1,m);lam=10**RNG.uniform(-2,1.5)
    S=four_code() if m==4 else hadamard(m);p=RNG.dirichlet(np.ones(m))
    phases=np.exp(1j*RNG.uniform(-np.pi,np.pi,m));phi=np.diag(np.sqrt(eta*p)*phases)@S
    raw=RNG.normal(size=(2*m,m))+1j*RNG.normal(size=(2*m,m));V=np.linalg.qr(raw)[0]
    amplitudes=V@phi;con=amplitudes[:m]
    C=np.mean(abs(np.diag(con))**2);T=np.sum(abs(con)**2)/m;E=T-C
    guess=RNG.uniform();vac=1-sum(eta*p)
    C+=guess*vac/m;E+=guess*vac*(m-1)/m
    check(f'arbitrary_POVM_{c}',max(0,C-lam*E-photon_score(eta,lam)['score']))

# 3. Independently solve small fixed-probe dual programs using PSD constraints.
# This is a general-purpose nonlinear solve of the dual, not a claim to have used an SDP solver.
optrows=[]
for c in range(12):
    eta=RNG.uniform(.12,1,4);lam=RNG.uniform(.4,8);o=photon_score(eta,lam);p=o['p'];q=eta*p
    phi=np.diag(np.sqrt(q))@four_code()
    Ws=[(1+lam)*np.outer(phi[:,j],phi[:,j])/4-lam*np.diag(q) for j in range(4)]
    def cons(y):return np.concatenate([np.linalg.eigvalsh(np.diag(y)-W) for W in Ws])
    res=minimize(lambda y:sum(y),np.full(4,1.),method='SLSQP',bounds=[(0,None)]*4,
                 constraints={'type':'ineq','fun':cons},options={'ftol':1e-11,'maxiter':1200})
    feasible_violation=max(0.,-cons(res.x).min());gap=abs(res.fun-o['score'])
    check(f'independent_dual_solver_{c}',max(feasible_violation,gap),2e-6)
    optrows.append({'case':c,'penalty':lam,'theorem':o['score'],'independent_dual':res.fun,
                    'abs_gap':gap,'max_psd_violation':feasible_violation,'solver_success':bool(res.success)})
savecsv('independent_dual_checks.csv',optrows)

# 4. Full frontier, not just exposed objectives.
front=[]
for r in [1,.8,.5,.2,.05]:
    eta=.7*np.array([1,1,1,r])
    for epsilon in [0,.0002,.001,.005,.02,.08,.15,.25,.5]:
        o=photon_frontier(eta,epsilon)
        check(f'error_budget_{r}_{epsilon}',max(0,o['E']-epsilon))
        check(f'normalization_{r}_{epsilon}',abs(o['C']+o['E']+o['F']-1))
        for lam in [.05,1/3,.7,2,5,20,100]:
            check(f'frontier_support_{r}_{epsilon}_{lam}',max(0,o['C']-lam*o['E']-photon_score(eta,lam)['score']))
        front.append({'t':.7,'r':r,'allowed_error':epsilon,'correct':o['C'],'wrong':o['E'],
                      'inconclusive':o['F'],'weak_path_probability':o['p'][-1],'branch':o['branch']})
savecsv('quantum_frontier.csv',front)

# 5. Uniform classical frontier: explicit POVM, including its failure effect.
uni=[]
for x in np.r_[np.geomspace(.0005,.1,12),np.linspace(.1,5,22)]:
    c=np.exp(-x);G=(1-c)*np.eye(4)+c*np.ones((4,4));sqrtG=roots(G);inv=np.linalg.inv(sqrtG)
    Eme=classical_uniform_frontier(float(x),1)['E']
    for frac in [0,.01,.1,.5,.9,1.]:
        E=frac*Eme;o=classical_uniform_frontier(float(x),float(E));C=o['C']
        T=(np.sqrt(C)*np.eye(4)+np.sqrt(E/3)*(np.ones((4,4))-np.eye(4)))@inv
        fail=np.eye(4)-T.conj().T@T
        check(f'classical_POVM_psd_{x}_{frac}',max(0,-np.linalg.eigvalsh(fail)[0]),2e-9)
        amps=T@sqrtG
        check(f'classical_POVM_rates_{x}_{frac}',max(abs(np.mean(abs(np.diag(amps))**2)-C),abs(np.sum(abs(amps)**2)/4-C-E)))
for eps in [0,.001,.01,.03,.05,.08,.1,.14,.2,.3]:
    q=photon_frontier([.7]*4,eps);cl=classical_uniform_frontier(.7,eps)
    uni.append({'error_budget':eps,'quantum_C':q['C'],'quantum_E':q['E'], 'classical_C_exact':cl['C'],'classical_E':cl['E']})
savecsv('uniform_exact_comparison.csv',uni)

# 6. Generic passive code maps, phase-referenced Grams, arbitrary measurements.
for case in range(300):
    m=[3,4,8][case%3];d=4;outs=4;As=[]
    for j in range(m):
        A=RNG.normal(size=(outs,d))+1j*RNG.normal(size=(outs,d));A/=np.linalg.svd(A,compute_uv=False)[0]
        As.append(A*RNG.uniform(.1,1))
    As=np.array(As);H,kappa=contrast_operator(As)
    alpha=RNG.normal(size=d)+1j*RNG.normal(size=d);alpha*=np.sqrt(10**RNG.uniform(-2,1.5)/np.vdot(alpha,alpha).real)
    N=float(np.vdot(alpha,alpha).real);betas=As@alpha
    G=np.exp(betas.conj()@betas.T-.5*np.sum(abs(betas)**2,axis=1)[:,None]-.5*np.sum(abs(betas)**2,axis=1)[None,:])
    overlap_sum=sum(abs(G[j,k]) for j in range(m) for k in range(j))
    check(f'code_pair_overlap_{case}',max(0,m*(m-1)/2*np.exp(-kappa*N)-overlap_sum))
    V=np.linalg.qr(RNG.normal(size=(m+4,m))+1j*RNG.normal(size=(m+4,m)))[0]
    amps=V@roots(G);C=np.mean(abs(np.diag(amps[:m]))**2);E=np.sum(abs(amps[:m])**2)/m-C
    bound=classical_correct_upper(kappa,N,float(E),m)
    check(f'generic_classical_bound_{case}',max(0,C-bound))
    lam=1/(m-1)+RNG.uniform(.01,8);b,nu=affine_classical_witness(kappa,RNG.uniform(.1,1),lam,m)
    check(f'affine_witness_{case}',max(0,C-lam*E-b-nu*N))
    radii=RNG.uniform(0,.03,m);true=As.copy()
    for j in range(m):
        R=RNG.normal(size=(outs,d))+1j*RNG.normal(size=(outs,d));R*=radii[j]/np.linalg.svd(R,compute_uv=False)[0];true[j]+=R
    kt=contrast_operator(true)[1];ku=robust_contrast_upper(kappa,radii)
    check(f'operator_radius_{case}',max(0,kt-ku))

# 7. Label-dependent "global" phases are not a coherent-probe gauge.
S=four_code();maps=np.array([np.diag(S[:,j]) for j in range(4)])
_,k0=contrast_operator(maps);changed=maps.copy();changed[0]*=-1
_,k1=contrast_operator(changed)
check('global_phase_original_kappa',k0-1);check('global_phase_changed_kappa',k1-4/3)
jsonsave('phase_gauge_warning.json',{'original_kappa':k0,'phase_changed_kappa':k1,
    'quantum_single_photon_density_matrices_unchanged':True,
    'warning':'Do not independently discard the global optical phase of each hidden setting.'})

# 8. Unbounded pulse-energy mixtures and tightness at symmetric low errors.
for case in range(250):
    kappa=RNG.uniform(.1,1.4);lam=RNG.uniform(1,20);weights=RNG.dirichlet(np.ones(7))
    energies=10**RNG.uniform(-5,3,7);mu=weights@energies
    C=E=0.
    for w,n in zip(weights,energies):
        Em=classical_uniform_frontier(kappa*n,1)['E'];eps=RNG.uniform()*Em
        o=classical_uniform_frontier(kappa*n,eps);C+=w*o['C'];E+=w*o['E']
    check(f'classical_flash_mixture_{case}',max(0,C-classical_correct_upper(kappa,mu,E)))
    b,nu=affine_classical_witness(kappa,.8,lam)
    check(f'classical_flash_affine_{case}',max(0,C-lam*E-b-nu*mu))

# 9. Exact photon-number/dark-click probabilities; phase averaging includes shared phases.
for r in [1,.8,.2]:
    eta=.7*np.array([1,1,1,r]);p=(1/eta)/np.sum(1/eta);H=4/np.sum(1/eta)
    for sigma in [0,.03,.1]:
        law=source_click_probabilities(eta,p,[0,1],1.,0.,sigma);rate=rates_from_masks(law)
        C=H*(.25+.75*np.exp(-sigma*sigma));E=H*.75*(1-np.exp(-sigma*sigma))
        check(f'phase_exact_{r}_{sigma}',max(abs(rate['C']-C),abs(rate['E']-E)))
    for n in [0,1,2,3]:
        pn=np.zeros(n+1);pn[n]=1;law=source_click_probabilities(eta,p,pn,[.7,.8,.9,.95],1e-5,.02)
        check(f'photon_counts_normalization_{r}_{n}',np.max(abs(law.sum(axis=1)-1)))

# Independent no-phase photon multinomial enumeration + Bernoulli dark flags.
eta=np.array([.8,.7,.6,.5]);p=RNG.dirichlet(np.ones(4));de=np.array([.8,.9,.85,.92]);dark=np.array([.002,.001,.003,.0015])
D=four_code()/2;pn=np.array([.1,.85,.05]);analytic=source_click_probabilities(eta,p,pn,de,dark,0.)
enum=np.zeros((4,16))
for j in range(4):
    w=de*abs(D@(np.sqrt(eta*p)*S[:,j]))**2;probs=np.r_[1-w.sum(),w]
    for n,mass in enumerate(pn):
        for outputs in itertools.product(range(5),repeat=n):
            pm=mass*np.prod([probs[o] for o in outputs]);mask=0
            for o in outputs:
                if o:mask|=1<<(o-1)
            for ds in range(16):
                pd=np.prod([dark[k] if ds>>k&1 else 1-dark[k] for k in range(4)])
                enum[j,mask|ds]+=pm*pd
check('independent_multinomial_dark_enumeration',np.max(abs(enum-analytic)))

# 10. Design forecasts: explicit hypothetical, NOT measured hardware specifications.
# Independent water-filling for the physical coherent nulling comparison.
def fill(eta,energy=1.):
    f=lambda ll:np.maximum((np.log(eta)-ll)/(4*eta),0)
    ll=brentq(lambda l:f(l).sum()-energy,-100,float(np.log(max(eta))))
    return f(ll)
forecast=[];configs={};pn=np.array([.029,.97,.001]);mu=float(np.arange(len(pn))@pn);penalty=5.
for r in [1.,.8,.5,.2,.05]:
    eta=.7*np.array([1,1,1,r]);o=photon_score(eta,penalty);law=source_click_probabilities(eta,o['p'],pn,.92,1e-6,.035)
    rate=rates_from_masks(law);score=rate['C']-penalty*rate['E']
    kU=robust_contrast_upper(.7,[.003]*4);muU=mu+.008;upper=classical_score_upper(kU,muU,penalty)
    coherent_mu=.99 if r==.05 else mu
    n=fill(eta,coherent_mu);claw=coherent_nulling_masks(eta,n,.92,1e-6,1e-4,.035);cl=rates_from_masks(claw);cs=cl['C']-penalty*cl['E']
    photon_robust=o['score']+2*(1+penalty)*.003
    forecast.append({'t':.7,'r':r,'quantum_C_model':rate['C'],'quantum_E_model':rate['E'],'quantum_F_model':rate['F'],
        'quantum_score_model':score,'classical_upper_robust':upper,'positive_expected_gap':score-upper,
        'coherent_nominal_mean':coherent_mu,'coherent_nulling_C_model':cl['C'],'coherent_nulling_E_model':cl['E'],'coherent_nulling_score_model':cs,
        'photon_score_upper_robust':photon_robust,'reverse_expected_gap':cs-photon_robust})
    configs[str(r)]={'eta':eta.tolist(),'p_quantum':o['p'].tolist(),'n_classical':n.tolist(),
                    'source_pn':pn.tolist(),'post_device_survival_and_detection':.92,'coherent_mean':coherent_mu,'coherent_mean_upper':1. if r==.05 else muU,'dark_per_gate':1e-6,'phase_sigma':.035,
                    'law_quantum':law.tolist(),'law_coherent_control':claw.tolist()}
savecsv('hypothetical_design_forecast.csv',forecast)
jsonsave('hypothetical_design_inputs.json',{'status':'HYPOTHETICAL_NOT_LAB_DATA','penalty':penalty,'mu':mu,'mu_upper':muU,
            'kappa_upper':kU,'per_map_operator_radius':.003,'conditions':configs})

# 11. Preparation change is optically testable with the same fixed decoder.
prep=[]
for r in [.8,.2,.05]:
    eta=.7*np.array([1,1,1,r])
    for lam in [1/3,1.,5.,20.]:
        o=photon_score(eta,lam)
        prep.append({'r':r,'penalty':lam,'p0':o['p'][0],'p1':o['p'][1],'p2':o['p'][2],'p3':o['p'][3],
                     'C':o['C'],'E':o['E'],'F':o['F'],'optimal_score':o['score']})
savecsv('preparation_recipes.csv',prep)

# 12. High-precision independent two-by-two reduction, rational test case.
with localcontext() as ctx:
    ctx.prec=75
    t=Decimal(7)/10;r=Decimal(4)/5;l=Decimal(5);a=(1+l)/4
    u=3*a-l;v=(a-l)*r;rad=((u-v)**2+12*a*a*r).sqrt()
    exact=t*(u+v+rad)/2
    check('75_digit_2x2_reduction',abs(float(exact)-photon_score([.7,.7,.7,.56],5)['score']))
    jsonsave('high_precision_check.json',{'decimal_digits':75,'score_decimal':str(exact),
                   'method':'Independent rational two-by-two symmetry reduction and Decimal square root; not interval certification.'})

# 13. Synthetic fixed-budget acceptance example; never relabelled as an experiment.
primary=forecast[1];N=500000
C=primary['quantum_C_model'];E=primary['quantum_E_model'];cnt={'correct':round(N*C),'wrong':round(N*E)};cnt['inconclusive']=N-sum(cnt.values())
cert=certify_counts(cnt,penalty,kU,muU,2.5e-4,5e-4)
cert['status']='SYNTHETIC_ROUNDED_EXPECTATION_NOT_AN_EXPERIMENT';cert['counts']=cnt
cert['multiphoton_tail_subtraction']=.002
cert['certified_gap_before_tail_subtraction']=cert['certified_gap']
cert['certified_gap']-=.002
cert['rejects_classical_null']=cert['certified_gap']>0
jsonsave('synthetic_certification_example.json',cert)
check('hypothetical_positive_test_has_margin',max(0,-cert['certified_gap']))
# Error handling exercises are part of the API contract.
for name,fun in [('zero_N',lambda:fixed_n_radius(0,5,.01)),('bad_phase_maps',lambda:contrast_operator(np.zeros((4,4)))),
 ('bad_error',lambda:classical_uniform_frontier(.7,1.1)),('bad_counts',lambda:certify_counts({'correct':2,'wrong':-1,'inconclusive':4},5,1,1,.01))]:
    try:fun()
    except (ValueError,TypeError):check('reject_'+name,0)
    else:raise AssertionError('did not reject '+name)
# 14. Complex flat codes, Gaussian coherent-control quadrature, and analysis accounting.
from scipy.integrate import quad
from analyze_trials import analyze
ERNG=np.random.default_rng(1729)
for m in [3,4,5,8]:
    F=np.exp(2j*np.pi*np.outer(np.arange(m),np.arange(m))/m)
    Z=np.exp(1j*ERNG.uniform(-np.pi,np.pi,m))[:,None]*F*np.exp(1j*ERNG.uniform(-np.pi,np.pi,m))[None,:]
    Z=Z[ERNG.permutation(m)][:,ERNG.permutation(m)]
    for case in range(8):
        eta=ERNG.uniform(.02,1,m);lam=ERNG.uniform(1/(m-1),20);o=photon_score(eta,lam)
        amp=(Z.conj().T/np.sqrt(m))@np.diag(np.sqrt(eta*o['p']))@Z
        C=np.mean(abs(np.diag(amp))**2);E=np.sum(abs(amp)**2)/m-C
        check(f'complex_flat_code_{m}_{case}',max(abs(C-o['C']),abs(E-o['E'])))
for case in range(8):
    eta=ERNG.uniform(.05,1,4);n=ERNG.dirichlet(np.ones(4))*ERNG.uniform(.1,1)
    de=ERNG.uniform(.7,1,4);dark=ERNG.uniform(0,1e-4,4);sigma=[0,.035,.08,.15][case%4];bg=1e-4
    law=coherent_nulling_masks(eta,n,de,dark,bg,sigma);ind=np.zeros((4,16))
    for j in range(4):
        no=[]
        for l in range(4):
            sign=-1 if l==j else 1
            integrand=lambda z: np.exp(-z*z/2-de[l]*(2*eta[l]*n[l]*(1-sign*np.cos(sigma*z))+bg))/np.sqrt(2*np.pi)
            val,err=quad(integrand,-12,12,epsabs=2e-13,epsrel=2e-13)
            no.append((1-dark[l])*val)
        for mask in range(16):ind[j,mask]=np.prod([1-no[l] if mask>>l&1 else no[l] for l in range(4)])
    check(f'independent_coherent_gaussian_integration_{case}',np.max(abs(law-ind)))
plan=json.loads((ROOT/'templates/primary_plan.example.json').read_text());plan['fixed_N']=64
records=[]
for j in range(4):
    for mask in range(16):
        records.append({'trial_id':str(16*j+mask),'condition_id':plan['condition_id'],
            'calibration_id':plan['calibration_id'],'phase_code_id':plan['phase_code_id'],
            'receiver_id':plan['receiver_id'],'hidden_label':str(j),'click_mask':str(mask)})
audit=analyze(plan,records,True)
check('analyzer_all_masks',sum(abs(audit['counts'][k]-v) for k,v in {'correct':4,'wrong':12,'inconclusive':48}.items()))
invalid=[('missing_trial',lambda:analyze(plan,records[:-1],True)),
         ('duplicate_id',lambda:analyze(plan,[records[0]]+records[:-1],True)),
         ('synthetic_guard',lambda:analyze(plan,records,False))]
for name,fn in invalid:
    try:fn()
    except ValueError:check('analyzer_reject_'+name,0)
    else:raise AssertionError('did not reject '+name)
reverse_plan=json.loads((ROOT/'templates/reverse_plan.example.json').read_text());reverse_plan['fixed_N']=64
reverse_rows=[dict(row,condition_id=reverse_plan['condition_id'],receiver_id=reverse_plan['receiver_id']) for row in records]
audit_reverse=analyze(reverse_plan,reverse_rows,True)
check('reverse_analyzer_counting',abs(audit_reverse['counts']['correct']-4))
reverse=forecast[-1];NN=50000
rcnt={'correct':round(NN*reverse['coherent_nulling_C_model']),'wrong':round(NN*reverse['coherent_nulling_E_model'])}
rcnt['inconclusive']=NN-sum(rcnt.values())
rtest=certify_reverse_counts(rcnt,5,[.7,.7,.7,.035],.003,2.5e-4,5e-4)
rtest['counts']=rcnt;rtest['status']='SYNTHETIC_ROUNDED_EXPECTATION_NOT_AN_EXPERIMENT'
jsonsave('synthetic_reverse_example.json',rtest)
check('synthetic_reverse_gap',max(0,-rtest['certified_gap']))
jsonsave('analyzer_accounting_check.json',{'status':'PASS','counts':audit['counts'],
        'invalid_inputs_rejected':len(invalid),'both_primary_tests_checked':True,'synthetic_only':True})

summary={'status':'PASS','checks':len(CHECKS),'seed':2026091417,'max_algebraic_residual':max(c['residual'] for c in CHECKS if not c['name'].startswith('independent_dual_solver')),
 'max_dual_solver_gap':max(r['abs_gap'] for r in optrows),'runtime_seconds':time.perf_counter()-START,
 'python':sys.version,'numpy':np.__version__,'scipy':scipy.__version__,'platform':platform.platform(),
 'sdp_solver_used':False,'interval_arithmetic_used':True,'lab_data_used':False,
 'scope':'Proof-backed results plus numerical diagnostics. Photon support uses exact-rational enclosures after audit repair 01; other calculations are not interval certified. Searches and tests are not substitutes for universal proofs.'}
jsonsave('validation.json',{'summary':summary,'checks':CHECKS});print(json.dumps(summary,indent=2));print('PRIMARY SYNTHETIC:',cert)
