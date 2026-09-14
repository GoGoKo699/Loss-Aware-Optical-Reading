"""Four-port receiver simulation with all threshold-detector records retained.

Source model: a specified distribution of Fock photon numbers in ONE prepared
spatial superposition, with independent Gaussian path phases (common to the
photons of one pulse). Does not claim to model a general multiphoton source.
The phase average is analytic, via Fourier moments, not independent phases per
photon. Higher source tails require a separate probability/energy bound.
"""
from __future__ import annotations
import itertools
import numpy as np
from numpy.typing import ArrayLike
from theory import four_code, transmissions


def _convolve(a:dict,b:dict)->dict:
    out={}
    for k,v in a.items():
        for l,w in b.items():
            key=tuple(x+y for x,y in zip(k,l));out[key]=out.get(key,0)+v*w
    return out


def source_click_probabilities(eta:ArrayLike,p:ArrayLike,pn:ArrayLike,
    detector_eff:ArrayLike, dark:ArrayLike, phase_sigma:float=0.,
    receiver:ArrayLike|None=None)->np.ndarray:
    """Return P[hidden_label, four_bit_mask]. 0 and multiple clicks are NOT dropped."""
    e=transmissions(eta);p=np.asarray(p,float);pn=np.asarray(pn,float)
    d=np.broadcast_to(np.asarray(detector_eff,float),(4,));dark=np.broadcast_to(np.asarray(dark,float),(4,))
    D=four_code()/2 if receiver is None else np.asarray(receiver,complex)
    if len(e)!=4 or p.shape!=(4,) or np.any(p<0) or not np.isclose(p.sum(),1):raise ValueError('invalid p')
    if pn.ndim!=1 or np.any(pn<0) or not np.isclose(pn.sum(),1):raise ValueError('pn must sum to one')
    if np.any((d<0)|(d>1)) or np.any((dark<0)|(dark>=1)) or phase_sigma<0:raise ValueError('invalid detector/noise parameters')
    if D.shape!=(4,4) or np.linalg.norm(D.conj().T@D-np.eye(4))>1e-8:raise ValueError('receiver must be unitary')
    code=four_code();basis=np.eye(4,dtype=int);zero=(0,)*4
    out=np.empty((4,16))
    for j in range(4):
        A=D*np.sqrt(e*p)[None,:]*code[:,j][None,:]
        noclick=np.empty(16)
        for subset in range(16):
            # u(phi)=1-probability of a detected photon in the selected ports.
            poly={zero:1.+0j}
            for l in range(4):
                if subset>>l&1:
                    for a in range(4):
                        for b in range(4):
                            freq=tuple(basis[a]-basis[b]);val=-d[l]*A[l,a]*A[l,b].conjugate()
                            poly[freq]=poly.get(freq,0)+val
            power={zero:1.+0j};val=0j
            for n,mass in enumerate(pn):
                if n:power=_convolve(power,poly)
                moment=sum(v*np.exp(-.5*phase_sigma**2*np.dot(k,k)) for k,v in power.items())
                val+=mass*moment
            if abs(val.imag)>1e-8:raise ArithmeticError('nonreal moment')
            factor=np.prod([1-dark[l] for l in range(4) if subset>>l&1])
            noclick[subset]=val.real*factor
        for mask in range(16):
            comp=15^mask;active=[l for l in range(4) if mask>>l&1];prob=0.
            for bits in range(1<<len(active)):
                sub=sum(1<<active[k] for k in range(len(active)) if bits>>k&1)
                prob+=(-1)**bits.bit_count()*noclick[comp|sub]
            out[j,mask]=prob
    if out.min() < -2e-10 or np.max(abs(out.sum(axis=1)-1))>2e-9:raise ArithmeticError('invalid mask law')
    return np.maximum(out,0)


def rates_from_masks(probs:ArrayLike)->dict:
    """One click -> port label; all other masks -> inconclusive. Fixed decoder."""
    P=np.asarray(probs,float)
    if P.shape!=(4,16) or np.max(abs(P.sum(axis=1)-1))>1e-8:raise ValueError('invalid P')
    C=sum(P[j,1<<j] for j in range(4))/4
    con=P[:,[1,2,4,8]].sum()/4
    return {'C':float(C),'E':float(con-C),'F':float(1-con),'conditional_correct':float(C/con) if con else None}


def coherent_nulling_masks(eta:ArrayLike,energies:ArrayLike,detector_eff:ArrayLike,
                           dark:ArrayLike,residual_background:float=0.,phase_sigma:float=0.)->np.ndarray:
    """Declared physical coherent competitor; ideal displacement background plus
    optional Poisson leakage background and Gaussian phase noise.
    Not the arbitrary-receiver bound.
    """
    e=transmissions(eta);n=np.asarray(energies,float);de=np.broadcast_to(np.asarray(detector_eff,float),(4,));da=np.broadcast_to(np.asarray(dark,float),(4,))
    if n.shape!=(4,) or np.any(n<0) or residual_background<0 or phase_sigma<0:raise ValueError('invalid energy')
    out=np.empty((4,16))
    nodes,weights=np.polynomial.hermite.hermgauss(36);weights/=np.sqrt(np.pi)
    phases=np.sqrt(2)*phase_sigma*nodes
    for j in range(4):
        click=np.empty(4)
        for l in range(4):
            sign=-1 if l==j else 1
            intensity=2*e[l]*n[l]*(1-sign*np.cos(phases))+residual_background
            noclick=(1-da[l])*np.sum(weights*np.exp(-de[l]*intensity))
            click[l]=1-noclick
        for mask in range(16):out[j,mask]=np.prod([click[l] if mask>>l&1 else 1-click[l] for l in range(4)])
    return out
