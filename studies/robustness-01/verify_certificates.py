"""Check stored witnesses, without invoking an optimizer.

Run with --results path/to/RESULTS.json --output NEW_DIRECTORY. Uses rational
model construction plus independent evaluation of the witness inequalities.
This certifies the finite rational models, not unknown physical hardware.
"""
from __future__ import annotations
import argparse,hashlib,itertools,json,math,platform,sys,time
from pathlib import Path
from fractions import Fraction as F
import numpy as np
import exact as ex
from exact import Q
from study import build,D,BASELINE


def verify(path,out):
    started=time.monotonic();r=json.loads(path.read_text());checks=[];counts={}
    def ck(name,condition):
        if not condition:raise AssertionError(name)
        checks.append(name)
    def pd(name,a):
        ck(name,ex.positive(a));counts['exact_positive_matrices']=counts.get('exact_positive_matrices',0)+1
    ck('baseline',r['baseline']==BASELINE and r['lambda']==5)
    for case in r['cases']:
        name=case['id'];spec=case['model'];A,A0,K,v,B,Rj=build(spec);I=ex.eye();Z=ex.zeros()
        idc=case['ideal'];iv=ex.decv(idc['vector']);norm=ex.norm2(iv)
        pd(name+'_ideal_support',ex.sub(ex.scale(I,F(idc['u'])),B))
        ck(name+'_ideal_feasible',F(idc['lower'])<=ex.expect(B,iv).r/norm<=F(idc['u']))
        # Rebuild each input measurement effect, without the study's payoff builder.
        effects=[]
        for row in D:
            projector=ex.outer([x.conj() for x in row])
            channel_effect=ex.add(ex.scale(projector,v),ex.scale(ex.diag([projector[i][i] for i in range(4)]),1-v))
            effects.append([ex.mul(ex.mul(ex.adj(a),channel_effect),a) for a in A])
        effects.append([ex.sub(I,ex.mul(ex.adj(a),a)) for a in A])
        def payoff(policy):
            mat=ex.zeros()
            for y,h in enumerate(policy):
                if h==4:continue
                for j in range(4):mat=ex.add(mat,ex.scale(effects[y][j],F(1 if h==j else -5,4)))
            return mat
        fc=case['fixed'];x=ex.decv(fc['input']);n=ex.norm2(x);q=payoff(fc['policy'])
        score=ex.expect(q,x).r/n
        ck(name+'_fixed_feasible_score',score==F(fc['lower_exact']) and F(fc['lower'])<=score)
        pols=[list(p)+[4] for p in itertools.product(range(5),repeat=4)] if fc['policies_checked']==625 else [[0,1,2,3,4],[4]*5]
        if len(pols)==625:
            ck(name+'_vacuum_common',all(effects[4][j]==effects[4][0] for j in range(4)))
        for k,p in enumerate(pols):pd(name+f'_policy_{k}',ex.sub(ex.scale(I,F(fc['upper_exact'])),payoff(p)))
        ck(name+'_fixed_upper_round',F(fc['upper'])>=F(fc['upper_exact']))
        jc=case['joint'];kind=spec['kind']
        if kind=='marked_phase':
            Y=ex.dec(jc['dual_Y']);total=Z
            for a in Rj:total=ex.add(total,a)
            pd(name+'_dual_positive',Y)
            for j,a in enumerate(Rj):
                W=ex.scale(ex.sub(ex.scale(a,6),ex.scale(total,5)),F(1,4))
                pd(name+f'_dual_state_{j}',ex.sub(Y,W))
            upper=max(Y[i][i].r for i in range(4))
            ck(name+'_dual_upper',upper==F(jc['upper_exact']) and F(jc['upper'])>=upper)
            factors=[ex.dec(f) for f in jc['effect_factors']];Ms=[ex.mul(a,ex.adj(a)) for a in factors];sm=Z
            for a in Ms:sm=ex.add(sm,a)
            c=F(jc['effect_scale']);pd(name+'_measurement_complete',ex.sub(ex.scale(I,c),sm))
            psi=ex.decv(jc['input']);nn=ex.norm2(psi);dd=ex.diag(psi);total_score=F(0)
            for j,a in enumerate(Rj):
                state=ex.mul(ex.mul(dd,a),ex.adj(dd))
                for h,M in enumerate(Ms):total_score+=F(1 if h==j else -5,4)*ex.tr(ex.mul(M,state)).r/(c*nn)
            ck(name+'_joint_lower',total_score==F(jc['lower_exact']) and F(jc['lower'])<=total_score)
            ck(name+'_gap_upper',F(case['regret']['upper'])>=upper-score)
            ck(name+'_gap_lower',F(case['regret']['lower'])<=max(F(0),total_score-F(fc['upper_exact'])))
        elif kind=='dephase':
            amps=[Q.of(float.fromhex(s)) for s in spec['amplitudes_hex']];eta=[a.r*a.r for a in amps]
            Bv=ex.add(ex.scale(ex.outer(amps),F(3,2)*v),ex.scale(ex.diag(eta),F(3,2)*(1-v)-5))
            sc=jc['support'];xx=ex.decv(sc['vector'])
            pd(name+'_dephase_support',ex.sub(ex.scale(I,F(sc['u'])),Bv))
            ck(name+'_dephase_rayleigh',F(sc['lower'])<=ex.expect(Bv,xx).r/ex.norm2(xx))
            ck(name+'_dephase_zero_regret',case['regret']['upper']==0 and 0<=v<=1)
            if v<=F(7,9):ck(name+'_all_abstain',jc['upper']==0 and fc['lower']==0)
        elif kind=='unitary':
            ck(name+'_unitary_exact',ex.mul(ex.adj(K),K)==I)
            ck(name+'_common_unitary',all(ex.mul(ex.adj(K),a)==b for a,b in zip(A,A0)))
            ck(name+'_unitary_gap',F(case['regret']['upper'])>=F(idc['u'])-score)
        else:
            R=__import__('study').rotation(F(spec['q']))
            coeff=[1,1,1,1-F(spec['amplitude_deficit'])]
            ck(name+'_contraction_eigenvalues',all(0<=s<=1 for s in coeff))
            ck(name+'_contraction_exact',K==ex.mul(ex.mul(R,ex.diag(coeff)),ex.adj(R)))
            ck(name+'_data_processing',all(ex.mul(K,a)==b for a,b in zip(A0,A)))
            ck(name+'_downstream_gap',F(case['regret']['upper'])>=F(idc['u'])-score)
        # Independence check: direct physical floating propagation and stored rates.
        xf=np.array([complex(z) for z in x]);xf/=np.linalg.norm(xf);df=ex.arr(D);Af=np.array([ex.arr(a) for a in A]);probs=[]
        for a in Af:
            u=a@xf;rho=float(v)*np.outer(u,u.conj())+(1-float(v))*np.diag(abs(u)**2)
            phot=np.real(np.diag(df@rho@df.conj().T));probs.append(np.r_[phot,1-np.vdot(u,u).real])
        C=E=0.
        for j,p in enumerate(probs):
            for y,h in enumerate(fc['policy']):
                if h==4:continue
                if h==j:C+=p[y]/4
                else:E+=p[y]/4
        ck(name+'_physical_rate_crosscheck',max(abs(C-fc['C']),abs(E-fc['E']),abs(1-C-E-fc['F']))<1e-12)
    # Uniform-loss closed forms provide an independent receiver and phase-model check.
    for c in r['cases']:
        s=c['model']
        if s['kind']!='marked_phase' or s['nominal_r']!=1 or len(s['phase_labels'])!=4:continue
        q=F(s['q']);h2=q*q/(1+q*q);amp=F(float.fromhex(s['amplitudes_hex'][0]));t=amp*amp
        standard=t*(1-F(9,2)*h2)
        ck(c['id']+'_uniform_D_formula',abs(float(standard)-c['fixed']['lower'])<1e-12)
        success=(math.sqrt(1+3*float(h2))+3*math.sqrt(1-float(h2)))**2/16
        feasible=float(t)*(6*success-5)
        ck(c['id']+'_explicit_four_port_receiver',feasible<=c['joint']['upper']+1e-12)
        ck(c['id']+'_four_port_near_dual',c['joint']['upper']-feasible<1e-7)
    summary={'status':'PASS','verified_cases':len(r['cases']),'checks':len(checks),**counts,
             'solver_called':False,'certified_object':'specified exact rational finite models, not calibration',
             'results_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'checks_passed':checks}
    out.mkdir(parents=True,exist_ok=False)
    (out/'VERIFICATION.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps({k:v for k,v in summary.items() if k!='checks_passed'},indent=2))
    print('seconds',time.monotonic()-started)

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--results',type=Path,required=True);p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    if args.output.exists():p.error('Use a new output directory')
    verify(args.results,args.output)
