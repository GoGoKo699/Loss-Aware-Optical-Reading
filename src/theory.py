"""Exact single-photon frontiers and conservative classical certificates.

All scores are per attempted, single-use interrogation, never postselected on a
click. Analytic proof and access assumptions are in proofs/THEORY.md.
"""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np
from numpy.typing import ArrayLike
from scipy.optimize import brentq


def transmissions(eta: ArrayLike) -> np.ndarray:
    a = np.asarray(eta, float)
    if a.ndim != 1 or a.size < 2 or not np.all(np.isfinite(a)) or np.any((a <= 0) | (a > 1)):
        raise ValueError('eta must be a finite vector of at least two values in (0,1]')
    return a


def four_code() -> np.ndarray:
    return np.ones((4,4)) - 2*np.eye(4)


def photon_score(eta: ArrayLike, penalty: float) -> dict:
    """Max C-penalty*E over one photon, an orthogonal flat phase code,
    any probe, and any final POVM. No occupied reference rail or idler.
    No-click random guessing is allowed only where it improves this score.
    """
    e = transmissions(eta); m = len(e)
    if not np.isfinite(penalty) or penalty < 0:
        raise ValueError('penalty must be finite and nonnegative')
    threshold = 1/(m-1)
    lam = max(float(penalty), threshold)
    v = np.sqrt(e)
    B = (1+lam)*np.outer(v,v)/m - lam*np.diag(e)
    eig, U = np.linalg.eigh(B)
    z = U[:,-1]
    if z.sum() < 0: z = -z
    p = z*z; p /= p.sum()
    C = float(np.sum(np.sqrt(e*p))**2/m)
    survival = float(e @ p); E = survival-C; F = 1-survival
    if penalty < threshold:
        C += F/m; E += (m-1)*F/m; F = 0.
    return {'penalty':float(penalty),'C':C,'E':max(0.,E),'F':max(0.,F),
            'score':C-penalty*E,'p':p,'amplitudes':np.sqrt(p),
            'eigenvalue':float(eig[-1]),'matrix':B}


def photon_secular(eta: ArrayLike, penalty: float) -> tuple[float,np.ndarray]:
    """Independent secular-equation calculation for penalty >= 1/(m-1)."""
    e=transmissions(eta);m=len(e)
    if penalty < 1/(m-1): raise ValueError('penalty below photon-only branch')
    f=lambda b: (1+penalty)/m*np.sum(e/(b+penalty*e))-1
    b=brentq(f,0,float(e.max())*(1+1e-10),xtol=2e-14)
    p=e/(b+penalty*e)**2; p/=p.sum()
    return float(b),p


def photon_frontier(eta: ArrayLike, error_budget: float) -> dict:
    """Exact optimal correct rate with E <= error_budget for a flat orthogonal code."""
    e=transmissions(eta);m=len(e)
    if not 0 <= error_budget <= 1: raise ValueError('error_budget outside [0,1]')
    H=m/np.sum(1/e)
    if error_budget == 0:
        p=(1/e)/np.sum(1/e)
        return {'C':H,'E':0.,'F':1-H,'p':p,'penalty':float('inf'), 'branch':'unambiguous'}
    edge=photon_score(e,1/(m-1)); E0=edge['E']; C0=edge['C'];F0=edge['F']
    Pme=C0+F0/m; Eme=1-Pme
    if error_budget >= Eme:
        return {'C':Pme,'E':Eme,'F':0.,'p':edge['p'],'penalty':0.,'branch':'minimum_error'}
    if error_budget >= E0-2e-14:
        u=m*(error_budget-E0)/(m-1)
        return {'C':C0+u/m,'E':error_budget,'F':max(0,F0-u),'p':edge['p'],
                'penalty':1/(m-1),'branch':'partial_vacuum_guessing'}
    lo=1/(m-1);hi=1.
    while photon_score(e,hi)['E']>error_budget:
        hi*=2
        if hi>1e8: raise ArithmeticError('Use the zero-error limit for such a small error budget')
    lam=brentq(lambda l:photon_score(e,l)['E']-error_budget,lo,hi,xtol=2e-12)
    out=photon_score(e,lam);out['branch']='retuned_preparation';return out


def classical_uniform_frontier(x: float, error_budget: float) -> dict:
    """Exact four-one-flip classical frontier for uniform loss and x=t*mu.
    Includes positive-P mixtures, labelled rare bright pulses and arbitrary receivers.
    """
    if x<0 or not np.isfinite(x) or not 0<=error_budget<=1: raise ValueError('invalid x or error')
    c=np.exp(-x);A=-np.expm1(-x)
    Pme=float((np.sqrt(1+3*c)+3*np.sqrt(A))**2/16)
    Eme=1-Pme
    E=min(error_budget,Eme)
    C=float((np.sqrt(A)+np.sqrt(E/3))**2) if E<Eme else Pme
    return {'C':C,'E':E,'F':max(0,1-C-E),'minimum_error_success':Pme,
            'branch':'curved' if error_budget<Eme else 'minimum_error'}


def contrast_operator(maps: ArrayLike) -> tuple[np.ndarray,float]:
    """H = sum_{j<k}(A_j-A_k)^dagger(A_j-A_k)/(m*(m-1)).
    Relative global optical phases of the A_j MUST be calibrated.
    """
    A=np.asarray(maps,complex)
    if A.ndim!=3 or len(A)<2 or not np.all(np.isfinite(A)): raise ValueError('maps must have shape (m,out,in)')
    m,o,d=A.shape;H=np.zeros((d,d),complex)
    for j in range(m):
        for k in range(j):
            diff=A[j]-A[k];H+=diff.conj().T@diff/(m*(m-1))
    H=(H+H.conj().T)/2
    return H,float(np.linalg.eigvalsh(H)[-1])


def robust_contrast_upper(kappa: float, radii: ArrayLike) -> float:
    """Valid when ||A_j-Ahat_j||_op <= radii[j] simultaneously."""
    r=np.asarray(radii,float);m=len(r)
    if m<2 or not np.isfinite(kappa) or kappa<0 or not np.all(np.isfinite(r)) or np.any(r<0): raise ValueError('invalid radius or contrast')
    delta2=sum((r[j]+r[k])**2 for j in range(m) for k in range(j))/(m*(m-1))
    return float((np.sqrt(kappa)+np.sqrt(delta2))**2)


def classical_correct_upper(kappa: float, mean_energy: float, error: float, m:int=4) -> float:
    if not np.all(np.isfinite([kappa,mean_energy,error])) or kappa<0 or mean_energy<0 or not 0<=error<=1 or m<2: raise ValueError('invalid bound input')
    A=-np.expm1(-kappa*mean_energy)
    return float(min(1-error,(np.sqrt(A)+np.sqrt(error/(m-1)))**2))


def classical_score_upper(kappa: float, mean_energy: float, penalty:float, m:int=4) -> float:
    if m<2 or not np.all(np.isfinite([kappa,mean_energy,penalty])) or kappa<0 or mean_energy<0 or penalty<=1/(m-1): raise ValueError('invalid support-bound input')
    K=(m-1)*penalty/((m-1)*penalty-1)
    return float(min(1., K*(-np.expm1(-kappa*mean_energy))))


def affine_classical_witness(kappa:float, reference_energy:float, penalty:float,m:int=4)->tuple[float,float]:
    """C-penalty*E <= b+nu*mu for every mean energy, no peak constraint."""
    if m<2 or not np.all(np.isfinite([kappa,reference_energy,penalty])) or kappa<0 or reference_energy<0 or penalty<=1/(m-1):raise ValueError('invalid witness inputs')
    K=(m-1)*penalty/((m-1)*penalty-1);x=kappa*reference_energy
    b=K*(1-(1+x)*np.exp(-x));nu=K*kappa*np.exp(-x)
    return float(b),float(nu)


def fixed_n_radius(n:int,penalty:float,alpha:float)->float:
    if not np.all(np.isfinite([n,penalty,alpha])) or n<1 or penalty<0 or not 0<alpha<1:raise ValueError('invalid statistical inputs')
    return float((1+penalty)*np.sqrt(np.log(1/alpha)/(2*n)))


def certify_counts(counts:dict,penalty:float,kappa_upper:float,mu_upper:float,
                   alpha_stat:float,alpha_calibration:float=0.,model_tv:float=0.)->dict:
    """Fixed-N, preregistered score. Requires iid trials or the stated conditional
    null-mean/cumulative predictable-budget contract. Calibration not inferred here.
    model_tv is a separately certified per-trial distance, not a fit residual.
    """
    if set(counts)!={'correct','wrong','inconclusive'}:raise ValueError('exactly three count keys required')
    if any(type(v) is not int or v<0 for v in counts.values()):raise ValueError('counts must be nonnegative integers')
    n=sum(counts.values());radius=fixed_n_radius(n,penalty,alpha_stat)
    if not 0<=model_tv<=1 or not 0<=alpha_calibration<1-alpha_stat:raise ValueError('invalid error allocation')
    score=(counts['correct']-penalty*counts['wrong'])/n
    upper=classical_score_upper(kappa_upper,mu_upper,penalty)+(1+penalty)*model_tv
    gap=score-radius-upper
    return {'N':n,'score':score,'statistical_radius':radius,'classical_upper':upper,
            'certified_gap':gap,'rejects_classical_null':gap>0,
            'familywise_error_upper':alpha_stat+alpha_calibration,
            'status':'CONDITIONAL_ON_EXTERNAL_CALIBRATION_AND_PREREGISTRATION'}


def certify_reverse_counts(counts:dict,penalty:float,eta_upper:ArrayLike,
                           operator_radius:float,alpha_stat:float,
                           alpha_calibration:float=0.)->dict:
    """Fixed-N measured coherent score versus ALL one-photon tested-path probes.
    Requires an external guarantee that incident coherent energy is <= one photon
    on average. No occupied quantum reference, retained idler, or repeat calls
    are included in the excluded one-photon architecture.
    """
    if set(counts)!={'correct','wrong','inconclusive'}:
        raise ValueError('exactly three count keys required')
    if any(type(v) is not int or v<0 for v in counts.values()):
        raise ValueError('counts must be nonnegative integers')
    if not np.isfinite(operator_radius) or operator_radius<0:
        raise ValueError('invalid operator radius')
    if not 0<=alpha_calibration<1-alpha_stat:
        raise ValueError('invalid error allocation')
    n=sum(counts.values()); radius=fixed_n_radius(n,penalty,alpha_stat)
    score=(counts['correct']-penalty*counts['wrong'])/n
    nominal=photon_score(eta_upper,penalty)['score']
    upper=min(1.,nominal+2*(1+penalty)*operator_radius)
    gap=score-radius-upper
    return {'N':n,'score':score,'statistical_radius':radius,
            'one_photon_upper':upper,'nominal_one_photon_upper':nominal,
            'certified_gap':gap,'rejects_four_path_one_photon_null':gap>0,
            'familywise_error_upper':alpha_stat+alpha_calibration,
            'status':'CONDITIONAL_ON_EXTERNAL_CALIBRATION_AND_PREREGISTRATION'}
