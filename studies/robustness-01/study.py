"""Bounded, four-mode C-5E robustness study. Writes only to a NEW output directory.

All model maps have exact rational complex entries. SDP proposals are generated
with SciPy linear-program cutting planes, then checked with exact rational LDL.
No CVXPY/SDP solver, canonical project module, lab data or network is used.
"""
from __future__ import annotations
import argparse, hashlib, itertools, json, math, platform, sys, time
from pathlib import Path
from fractions import Fraction as F
import numpy as np
import scipy
from scipy.optimize import linprog
import exact as ex
from exact import Q

BASELINE='de73c9b094036b756d1ff008eaccbc52cec46207'
LAMBDA=5
D=ex.mat(np.ones((4,4))/2-np.eye(4))
I=ex.eye();ZERO=ex.zeros()


def phase(q):return Q((1-q*q)/(1+q*q),2*q/(1+q*q))
def rotation(q):
    c=phase(q);a=ex.eye();a[0][0]=a[3][3]=Q(c.r)
    a[0][3]=Q(-c.i);a[3][0]=Q(c.i);return a

def models():
    ret=[]
    for r in [1.,.8,.2]:
        amps=[float(math.sqrt(.7))]*3+[float(math.sqrt(.7*r))]
        base={'amplitudes_hex':[v.hex() for v in amps],'nominal_t':.7,'nominal_r':r}
        for q in [F(0),F(1,100),F(1,40),F(1,20),F(1,10)]:
            ret.append(dict(base,id=f'phase_r{r:g}_q{q.numerator}-{q.denominator}',kind='marked_phase',q=str(q),phase_labels=[0,1,2,3]))
        if r!=1:
            ret.append(dict(base,id=f'single_phase_r{r:g}',kind='marked_phase',q='1/20',phase_labels=[3]))
            for vis in ['1','999/1000','99/100','19/20','4/5','77/100']:
                ret.append(dict(base,id=f'dephase_r{r:g}_v{vis.replace("/","-")}',kind='dephase',visibility=vis))
            for q in ['1/100','1/20','1/10']:
                ret.append(dict(base,id=f'unitary_r{r:g}_q{q.replace("/","-")}',kind='unitary',q=q))
            for d in ['1/400','1/100','1/40']:
                ret.append(dict(base,id=f'distributed_r{r:g}_d{d.replace("/","-")}',kind='distributed_loss',q='1/10',amplitude_deficit=d))
    return ret


def build(spec):
    a=[Q.of(float.fromhex(s)) for s in spec['amplitudes_hex']];T=ex.diag(a)
    nom=[]
    for j in range(4):
        phases=[Q.of(-1 if i==j else 1) for i in range(4)]
        nom.append(ex.mul(T,ex.diag(phases)))
    A=nom;kind=spec['kind'];v=F(1);K=I
    if kind=='marked_phase':
        A=[]
        for j in range(4):
            z=[Q.of(1) for _ in range(4)];z[j]=-phase(F(spec['q'])) if j in spec['phase_labels'] else Q.of(-1)
            A.append(ex.mul(T,ex.diag(z)))
    elif kind=='unitary':K=rotation(F(spec['q']));A=[ex.mul(K,x) for x in nom]
    elif kind=='distributed_loss':
        R=rotation(F(spec['q']));K=ex.mul(ex.mul(R,ex.diag([1,1,1,1-F(spec['amplitude_deficit'])])),ex.adj(R));A=[ex.mul(K,x) for x in nom]
    elif kind=='dephase':v=F(spec['visibility'])
    else:raise ValueError(kind)
    eta=[x.r*x.r for x in a]
    B=ex.sub(ex.scale(ex.outer(a),F(3,2)),ex.scale(ex.diag(eta),5))
    Rj=[]
    if kind in ('marked_phase','dephase'):
        for x in A:
            vv=[x[i][i] for i in range(4)]
            Rj.append(ex.add(ex.scale(ex.outer(vv),v),ex.scale(ex.diag(eta),1-v)))
    return A,nom,K,v,B,Rj


def input_effects(A,v=F(1),decoder=D):
    effects=[]
    for y in range(4):
        P=ex.outer([decoder[y][i].conj() for i in range(4)])
        P=ex.add(ex.scale(P,v),ex.scale(ex.diag([P[i][i] for i in range(4)]),1-v))
        effects.append([ex.mul(ex.mul(ex.adj(a),P),a) for a in A])
    effects.append([ex.sub(I,ex.mul(ex.adj(a),a)) for a in A])
    return effects


def payoff(effects):
    W=[]
    for eff in effects:
        sm=ex.zeros()
        for a in eff:sm=ex.add(sm,a)
        W.append([ex.scale(ex.sub(ex.scale(a,6),ex.scale(sm,5)),F(1,4)) for a in eff]+[ZERO])
    return W


def policy_matrix(W,pol):
    out=ex.zeros()
    for y,j in enumerate(pol):out=ex.add(out,W[y][j])
    return out


def fixed_certificate(A,v=F(1),all_policies=True):
    W=payoff(input_effects(A,v));pols=[list(x)+[4] for x in itertools.product(range(5),repeat=4)] if all_policies else [[0,1,2,3,4],[4,4,4,4,4]]
    wf=np.array([[ex.arr(z) for z in row] for row in W])
    qs=np.array([wf[np.arange(5),p].sum(axis=0) for p in pols])
    vals,vecs=np.linalg.eigh(qs);imax=int(np.argmax(vals[:,-1]));pol=pols[imax]
    M=policy_matrix(W,pol);x=[Q.of(z) for z in vecs[imax,:,-1]]
    n=ex.norm2(x);lower=ex.expect(M,x).r/n
    slack=1e-9;u=F(float(vals[imax,-1]+slack));ok=False
    while not ok:
        ok=True
        for p in pols:
            if not ex.positive(ex.sub(ex.scale(I,u),policy_matrix(W,p))):ok=False;break
        if not ok:
            slack*=10;u=F(float(vals[imax,-1]+slack))
            if slack>1e-3:raise ArithmeticError('Fixed policy upper not certified')
    effects=input_effects(A,v)
    C=F(0);E=F(0)
    for y,h in enumerate(pol):
        if h==4:continue
        for j in range(4):
            prob=ex.expect(effects[y][j],x).r/(4*n)
            if j==h:C+=prob
            else:E+=prob
    assert C-5*E==lower
    return {'lower':ex.down(lower),'upper':ex.up(u),'upper_exact':str(u),
            'lower_exact':str(lower),'input':ex.encv(x),'policy':pol,
            'policies_checked':len(pols),'C':float(C),'E':float(E),'F':float(1-C-E),
            'scope':'complete fixed-optics optimum; vacuum has no information' if all_policies else 'best of standard labels and all-abstention; lower bound, not fixed-optics optimum'}


BASIS=[]
for i in range(4):
    a=np.zeros((4,4),complex);a[i,i]=1;BASIS.append(a)
for i in range(4):
    for j in range(i+1,4):
        a=np.zeros((4,4),complex);a[i,j]=a[j,i]=1;BASIS.append(a)
        a=np.zeros((4,4),complex);a[i,j]=1j;a[j,i]=-1j;BASIS.append(a)
BASIS=np.array(BASIS)


def diagonal_dual(Rj,tol=2e-8,maxiter=300):
    """LP is a proposal generator; only exact checked certificates are reported."""
    total=ZERO
    for x in Rj:total=ex.add(total,x)
    Ws=[ex.scale(ex.sub(ex.scale(x,6),ex.scale(total,5)),F(1,4)) for x in Rj]+[ZERO]
    wf=np.array([ex.arr(w) for w in Ws]);rows=[];rhs=[];tags=[];vec=[];solver_events=[]
    def cut(k,v):
        coeff=np.einsum('i,aij,j->a',v.conj(),BASIS,v).real
        rows.append(np.r_[-coeff,0.]);rhs.append(-float(np.vdot(v,wf[k]@v).real));tags.append(k);vec.append(v)
    for k in range(5):
        for v in np.eye(4):cut(k,v)
        _,V=np.linalg.eigh(wf[k])
        for v in V.T:cut(k,v)
    res=None
    for it in range(maxiter):
        cs=np.c_[np.eye(4),np.zeros((4,12)),-np.ones(4)]
        args=dict(c=np.r_[np.zeros(16),1.],A_ub=np.r_[cs,rows],b_ub=np.r_[np.zeros(4),rhs],bounds=[(None,None)]*17)
        trial=linprog(**args,method='highs',options={'dual_feasibility_tolerance':1e-9,'primal_feasibility_tolerance':1e-9})
        if not trial.success:
            solver_events.append({'iteration':it,'method':'highs','message':trial.message})
            trial=linprog(**args,method='highs-ipm',options={'dual_feasibility_tolerance':1e-8,'primal_feasibility_tolerance':1e-8})
        if not trial.success:
            solver_events.append({'iteration':it,'method':'highs-ipm','message':trial.message})
            if res is None:raise ArithmeticError('No usable LP iterate')
            break
        res=trial;Y=np.einsum('a,aij->ij',res.x[:16],BASIS);err=0.
        for k in range(5):
            es,Vs=np.linalg.eigh(Y-wf[k]);err=max(err,-float(es[0]))
            for ix in np.where(es < -tol/5)[0]:cut(k,Vs[:,ix])
        if err<tol:break
    assert res is not None
    # Store EXACT rational Hermitian Y and verify the dual inequalities.
    Yr=ex.mat(Y);delta=F(float(max(0,err)+1e-9))
    while True:
        Yu=ex.add(Yr,ex.scale(I,delta))
        if all(ex.positive(ex.sub(Yu,w)) for w in Ws):break
        delta*=10
        if delta>1:raise ArithmeticError('Dual certificate verification failed')
    upper=max(Yu[i][i].r for i in range(4))
    # Reconstruct a feasible physical POVM from LP dual weights, independently
    # factor it, and scale it down using an exact positive-completeness check.
    X=np.zeros((5,4,4),complex)
    for w,k,v in zip(-res.ineqlin.marginals[4:],tags,vec):X[k]+=max(0,float(w))*np.outer(v,v.conj())
    p=np.maximum(-res.ineqlin.marginals[:4],1e-14);p/=p.sum();inputv=[Q.of(float(x)) for x in np.sqrt(p)]
    inv=np.diag(1/np.sqrt(p));factors=[];N=[]
    for x in X[:4]:
        m=inv@x@inv;e,V=np.linalg.eigh((m+m.conj().T)/2)
        fac=ex.mat(V*np.sqrt(np.maximum(0,e)));factors.append(fac);N.append(ex.mul(fac,ex.adj(fac)))
    totalN=ZERO
    for x in N:totalN=ex.add(totalN,x)
    scale=F(float(max(1,np.linalg.eigvalsh(ex.arr(totalN))[-1])+1e-9))
    while not ex.positive(ex.sub(ex.scale(I,scale),totalN)):scale+=F(1,10**8)
    diagv=ex.diag(inputv);norm=ex.norm2(inputv);C=F(0);T=F(0)
    for j,rho in enumerate(Rj):
        actual=ex.mul(ex.mul(diagv,rho),ex.adj(diagv))
        C+=ex.tr(ex.mul(N[j],actual)).r/(4*scale*norm)
        T+=ex.tr(ex.mul(totalN,actual)).r/(4*scale*norm)
    lower=6*C-5*T
    if lower>upper:raise AssertionError('Primal-dual order')
    return {'lower':ex.down(lower),'upper':ex.up(upper),'lower_exact':str(lower),'upper_exact':str(upper),
            'dual_Y':ex.enc(Yu),'input':ex.encv(inputv),'effect_factors':[ex.enc(f) for f in factors],
            'effect_scale':str(scale),'iterations':it+1,'LP_residual':err,'solver_events':solver_events,
            'C':float(C),'E':float(T-C),'F':float(1-T),'exact_dual_checked':True,'exact_measurement_checked':True}


def standard_rate(A,psi,V=D,v=F(1)):
    effects=input_effects(A,v,V);n=ex.norm2(psi)
    C=sum((ex.expect(effects[j][j],psi).r for j in range(4)),F(0))/(4*n)
    T=sum((ex.expect(effects[y][j],psi).r for y in range(4) for j in range(4)),F(0))/(4*n)
    return C,T-C,1-T


def run(out):
    start=time.monotonic();cases=[];certs=[];ledger=[]
    def check(name,condition,value=None):
        ledger.append({'name':name,'pass':bool(condition),'value':value})
        if not condition:raise AssertionError(name)
    for spec in models():
        t0=time.monotonic();A,A0,K,v,B,Rj=build(spec);ideal,iv=ex.eigen_certificate(B)
        kind=spec['kind'];ph=kind=='marked_phase'
        fixed=fixed_certificate(A,v,all_policies=ph)
        record={'id':spec['id'],'model':spec,'fixed':fixed,'ideal':ideal}
        if ph:
            joint=diagonal_dual(Rj);record['joint']=joint
            gapL=max(F(0),F(joint['lower_exact'])-F(fixed['upper_exact']))
            gapU=max(F(0),F(joint['upper_exact'])-F(fixed['lower_exact']))
            record['regret']={'lower':ex.down(gapL),'upper':ex.up(gapU),'scope':'global optimum minus full fixed-optics optimum'}
        elif kind=='dephase':
            a=[Q.of(float.fromhex(s)) for s in spec['amplitudes_hex']];eta=[x.r*x.r for x in a]
            Bv=ex.add(ex.scale(ex.outer(a),F(3,2)*v),ex.scale(ex.diag(eta),F(3,2)*(1-v)-5))
            opt,ov=ex.eigen_certificate(Bv);beta=max(F(0),F(opt['u']))
            record['joint']={'lower':max(0,opt['lower']),'upper':ex.up(beta),'proof':'symmetric dephasing theorem','support':opt}
            record['regret']={'lower':0.,'upper':0.,'scope':'exact theorem: optimized input and suitable abstention'}
            c,e,f=standard_rate(A,ov,v=v)
            check(spec['id']+'_saturation',abs(float(c-5*e)-opt['lower'])<1e-12)
        elif kind=='unitary':
            c,e,f=standard_rate(A,iv,V=ex.mul(D,ex.adj(K)))
            check(spec['id']+'_calibration_invariance',abs(float(c-5*e)-ideal['lower'])<1e-12)
            record['joint']={'lower':ideal['lower'],'upper':ideal['upper'],'proof':'common output-unitary invariance'}
            record['calibrated_score']=float(c-5*e)
            record['regret']={'lower':0.,'upper':ex.up(max(F(0),F(ideal['u'])-F(fixed['lower_exact']))),'scope':'uncalibrated standard readout upper regret; calibrated optimum gap is exactly zero'}
        else:
            record['joint']={'lower':fixed['lower'],'upper':ideal['upper'],'proof':'data processing under common downstream contraction'}
            record['regret']={'lower':0.,'upper':ex.up(max(F(0),F(ideal['u'])-F(fixed['lower_exact']))),'scope':'upper bound; includes possible information loss and is not asserted tight'}
        eps=max(ex.norm_upper(ex.sub(a,b)) for a,b in zip(A,A0))
        record['generic_map_radius']=ex.up(eps)
        record['generic_regret_upper']=min(1.,ex.up(24*eps)) if kind!='dephase' else None
        # P1 screening only: ideal single-photon input, mean budget 1, uniform
        # downstream survival 0.92, no dark counts or source impurity. Noise is
        # not used to weaken the all-classical ceiling.
        H=ZERO
        for j in range(4):
            for k in range(j+1,4):
                dif=ex.sub(A[j],A[k]);H=ex.add(H,ex.scale(ex.mul(ex.adj(dif),dif),F(1,12)))
        hc,_=ex.eigen_certificate(H);kappa=hc['upper']
        Ucl=min(1,(15/14)*(-math.expm1(-kappa)))
        stat=6*math.sqrt(math.log(1/.00025)/(2*500000))
        record['P1_illustrative']={'mean_budget':1.,'uniform_downstream_survival':.92,
                'classical_upper_nominal':Ucl,'post_readout_score':.92*fixed['lower'],
                'statistical_radius':stat,'screen_margin':.92*fixed['lower']-Ucl-stat,
                'status':'IDEAL_SOURCE_SCREEN_NOT_CALIBRATION_OR_A_STATISTICAL_CERTIFICATE'}
        check(spec['id']+'_score_valid',fixed['lower']<=record['joint']['upper']+1e-10)
        check(spec['id']+'_probabilities',min(fixed['C'],fixed['E'],fixed['F'])>=-1e-13)
        check(spec['id']+'_passive',all(np.linalg.norm(ex.arr(a),2)<=1+1e-14 for a in A))
        cases.append(record)
        print(spec['id'],'fixed',round(fixed['lower'],9),'joint',round(record['joint']['lower'],9),round(record['joint']['upper'],9),'gap',record['regret'],'seconds',round(time.monotonic()-t0,2),flush=True)
    # Independently sampled input/POVM diagnostic for the analytic dephasing bound.
    rng=np.random.default_rng(2026091503)
    for vis in [F(77,100),F(4,5),F(19,20),F(99,100),F(1)]:
        spec=dict(models()[0],kind='dephase',visibility=str(vis))
        A,_,_,v,B,Rj=build(spec)
        a=np.sqrt([float.fromhex(x)**2 for x in spec['amplitudes_hex']])
        Bv=1.5*float(v)*np.outer(a,a)+(1.5*(1-float(v))-5)*np.diag(a*a)
        bound=max(0,float(np.linalg.eigvalsh(Bv)[-1]));rf=np.array([ex.arr(r) for r in Rj])
        for i in range(40):
            psi=rng.normal(size=4)+1j*rng.normal(size=4);psi/=np.linalg.norm(psi)
            rand=rng.normal(size=(20,4))+1j*rng.normal(size=(20,4));Qis=np.linalg.qr(rand)[0]
            Ms=np.array([x.conj().T@x for x in Qis.reshape(5,4,4)])
            states=np.einsum('i,jik,k->jik',psi,rf,psi.conj());C=sum(np.trace(Ms[j]@states[j]).real for j in range(4))/4
            T=sum(np.trace(Ms[:4].sum(0)@states[j]).real for j in range(4))/4
            check(f'random_dephase_{vis}_{i}',6*C-5*T<=bound+1e-12)
    # Generic continuity: actual state distance compared to 2||A-A0||, including vacuum.
    for i in range(40):
        a=(rng.normal(size=(4,4))+1j*rng.normal(size=(4,4)))/5
        a/=max(1,np.linalg.norm(a,2));b=a+1e-3*(rng.normal(size=(4,4))+1j*rng.normal(size=(4,4)))
        b/=max(1,np.linalg.norm(b,2));psi=rng.normal(size=4)+1j*rng.normal(size=4);psi/=np.linalg.norm(psi)
        u=a@psi;w=b@psi;dif=np.outer(u,u.conj())-np.outer(w,w.conj());vac=np.vdot(w,w).real-np.vdot(u,u).real
        dist=(np.abs(np.linalg.eigvalsh(dif)).sum()+abs(vac))/2
        check(f'continuity_{i}',dist<=2*np.linalg.norm(a-b,2)+1e-13)
    result={'status':'PASS','baseline':BASELINE,'lambda':5,'case_count':len(cases),'checks':len(ledger),'cases':cases,'ledger':ledger,
            'lab_data':False,'priority_claim':False,'scope':'Four-mode tolerance screen; exact rational certificates only for specified finite models, not calibration or all numeric routines.'}
    out.mkdir(parents=True,exist_ok=False)
    (out/'RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    env={'python':sys.version,'numpy':np.__version__,'scipy':scipy.__version__,'platform':platform.platform(),
         'elapsed_seconds':time.monotonic()-start,'uses_canonical_module':False,'uses_sdp_solver':False,
         'optimizer':'SciPy linprog (HiGHS) spectral cutting planes; proposal only',
         'certification':'exact rational Hermitian LDL plus rational primal scores',
         'input_semantics':'exact rational maps from binary64 amplitude values and rational unit-circle parametrizations',
         'lab_data':False,'network':False}
    (out/'ENVIRONMENT.json').write_text(json.dumps(env,indent=2)+'\n')
    print('PASS',len(cases),'cases',len(ledger),'diagnostics',flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    out=args.output.resolve()
    if out.exists():p.error('Output must be a new directory')
    run(out)
