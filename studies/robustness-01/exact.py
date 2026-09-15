"""Small exact complex-rational matrix checks. No numerical optimizer is trusted.

Float inputs are interpreted as their exact binary values. Strict LDL positivity
is a sufficient certificate; failure is not proof of non-positivity.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction as F
import math
import numpy as np

@dataclass(frozen=True)
class Q:
    r: F = F(0)
    i: F = F(0)
    @staticmethod
    def of(x):
        if isinstance(x,Q): return x
        if isinstance(x,complex) or np.iscomplexobj(x):return Q(F(float(x.real)),F(float(x.imag)))
        return Q(F(x))
    def __add__(self,x):
        x=Q.of(x);return Q(self.r+x.r,self.i+x.i)
    __radd__=__add__
    def __neg__(self):return Q(-self.r,-self.i)
    def __sub__(self,x):return self+-Q.of(x)
    def __rsub__(self,x):return Q.of(x)+-self
    def __mul__(self,x):
        x=Q.of(x);return Q(self.r*x.r-self.i*x.i,self.r*x.i+self.i*x.r)
    __rmul__=__mul__
    def __truediv__(self,x):
        x=Q.of(x);d=x.r*x.r+x.i*x.i
        return self*x.conj()*Q(1/d)
    def conj(self):return Q(self.r,-self.i)
    def __complex__(self):return complex(float(self.r),float(self.i))
    def l1(self):return abs(self.r)+abs(self.i)

Z=Q();ONE=Q(F(1))
def zeros(n=4,m=None):return [[Z for _ in range(n if m is None else m)] for _ in range(n)]
def eye(n=4):return [[ONE if i==j else Z for j in range(n)] for i in range(n)]
def mat(a):return [[Q.of(x) for x in row] for row in a]
def arr(a):return np.array([[complex(x) for x in row] for row in a])
def adj(a):return [[a[j][i].conj() for j in range(len(a))] for i in range(len(a[0]))]
def add(a,b):return [[x+y for x,y in zip(ar,br)] for ar,br in zip(a,b)]
def scale(a,c):return [[x*c for x in row] for row in a]
def sub(a,b):return add(a,scale(b,-1))
def mul(a,b):return [[sum((a[i][k]*b[k][j] for k in range(len(b))),Z) for j in range(len(b[0]))] for i in range(len(a))]
def outer(v):return [[x*y.conj() for y in v] for x in v]
def diag(v):return [[Q.of(v[i]) if i==j else Z for j in range(len(v))] for i in range(len(v))]
def tr(a):return sum((a[i][i] for i in range(len(a))),Z)
def expect(a,v):
    return sum((v[i].conj()*a[i][j]*v[j] for i in range(len(v)) for j in range(len(v))),Z)
def norm2(v):return sum((x.r*x.r+x.i*x.i for x in v),F(0))
def positive(a):
    """Exact Hermitian LDL test for positive definiteness."""
    n=len(a)
    if a!=adj(a):return False
    L=eye(n);d=[]
    for k in range(n):
        pivot=a[k][k]-sum((L[k][j]*L[k][j].conj()*d[j] for j in range(k)),Z)
        if pivot.i or pivot.r<=0:return False
        d.append(pivot.r)
        for i in range(k+1,n):
            L[i][k]=(a[i][k]-sum((L[i][j]*L[k][j].conj()*d[j] for j in range(k)),Z))/d[k]
    return True

def up(f):
    x=float(f)
    if F(x)<f:x=math.nextafter(x,math.inf)
    return x

def down(f):
    x=float(f)
    if F(x)>f:x=math.nextafter(x,-math.inf)
    return x

def enc(a):return [[[str(x.r),str(x.i)] for x in row] for row in a]
def dec(a):return [[Q(F(x[0]),F(x[1])) for x in row] for row in a]
def encv(v):return [[str(x.r),str(x.i)] for x in v]
def decv(v):return [Q(F(x[0]),F(x[1])) for x in v]

def eigen_certificate(a,slack=1e-10):
    e,V=np.linalg.eigh(arr(a));v=[Q.of(x) for x in V[:,-1]]
    lower=expect(a,v).r/norm2(v)
    u=F(float(e[-1]+slack))
    while not positive(sub(scale(eye(len(a)),u),a)):
        slack*=10;u=F(float(e[-1]+slack))
        if slack>1:raise ArithmeticError('Could not certify eigenvalue upper')
    return {'lower':down(lower),'upper':up(u),'u':str(u),'vector':encv(v)},v

def sqrt_upper(f):
    if f<0:raise ValueError('negative square')
    x=F(math.sqrt(float(f)))
    if x*x<f:x=F(math.nextafter(float(x),math.inf))
    while x*x<f:x=F(math.nextafter(float(x),math.inf))
    return x

def norm_upper(a):
    b=mul(adj(a),a)
    bound=max((b[i][i].r+sum((b[i][j].l1() for j in range(len(b)) if j!=i),F(0)) for i in range(len(b))),default=F(0))
    return sqrt_upper(bound)
