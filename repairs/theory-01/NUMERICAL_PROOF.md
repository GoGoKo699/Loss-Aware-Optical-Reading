# Why the repaired photon support bound encloses the optimum

This is an implementation argument for the theorem already audited. It introduces
no new optical model, physical claim, or novelty assertion.

## 1. A monotone equation without large cancellation

For lambda >= 1/(m-1), the unique positive support value beta satisfies

$$
\frac{1+\lambda}{m}\sum_i\frac{\eta_i}{\beta+\lambda\eta_i}=1.
$$

Set u=1/(1+lambda) and s=lambda/(1+lambda). Algebra gives the equivalent equation

$$
g(\beta)=\sum_i\frac{\beta}{s\eta_i+u\beta}-m=0.
$$

Every term has derivative s eta_i/(s eta_i+u beta)^2 > 0. Thus g is strictly
increasing. The harmonic mean H=m/(sum_i 1/eta_i) is a feasible zero-error score,
so the established variational theorem gives H <= beta. The root is also no
larger than max eta_i: at that point every denominator is at most beta, hence
g(beta) >= 0. The implementation independently checks both bracket signs.

There is no subtraction of eigenvalues or probabilities of size lambda.
As lambda increases, this equation approaches beta sum_i(1/eta_i)=m directly.

## 2. Exact endpoint signs

The input values are converted to `Fraction` from their binary64 floats. This
represents their exact binary values, not the ideal decimal strings they might
have originated from. Every evaluation of g uses rational arithmetic, so its
sign has no floating-point tolerance.

Positive binary64 numbers are ordered by their unsigned bit representation.
Integer bisection between a downward-rounded H and max eta_i therefore terminates
at equal or adjacent floats in at most 63 steps. A negative residual retains the
lower endpoint; a positive residual retains the upper. A rational zero is exact.
Both final signs are checked again. Strict monotonicity proves

$$
\beta_{\rm lower}\le\beta\le\beta_{\rm upper}.
$$

This is an algorithmic enclosure argument, not a conclusion from a finite test
set. It relies on integer/Fraction arithmetic and the documented binary64 input
format. No statement about the correctness of arbitrary Python interpreters is made.

## 3. The low-penalty branch

For lambda below the exact rational threshold, first enclose beta0 at
lambda0=1/(m-1). The audited theorem gives

$$
P_{\rm ME}=\frac{1+(m-1)\beta_0}{m},\qquad
\beta(\lambda)=(1+\lambda)P_{\rm ME}-\lambda.
$$

The coefficient of beta0 is positive. Applying this affine map with rational
arithmetic transports its enclosure. Float conversion is checked against the
exact rational and moved one representable step outward when necessary. The
final comparison verifies the requested rounding direction. This also handles
the small discrepancy between a floating representation of lambda0 and lambda0.

## 4. Nominal rates

The recipe is evaluated from the bracket midpoint using

$$
p_i\ \mathrel{\propto}\ \frac{\eta_i}{(s\eta_i+u\beta)^2}.
$$

With a_i=sqrt(eta_i p_i) and abar=(sum_i a_i)/m,

$$
C=m\bar a^2,\qquad E=\sum_i(a_i-\bar a)^2.
$$

This is equivalent to the pairwise-difference formula in the audit and avoids
survival-minus-C cancellation. A 90-digit decimal calculation supplies nominal
rates. Their float values are not used to certify the upper endpoint. This
separation is necessary: numerically displaying a good input does not prove an
upper bound on all inputs.

## 5. Reverse certificate

If U is the certified photon-support upper endpoint and epsilon is the supplied
nonnegative operator radius, the existing theorem bounds the perturbed score by

$$
\min\{1,U+2(1+\lambda)\epsilon\}.
$$

The addition, multiplication, and minimum are performed on exact rationals
representing the supplied floats, followed by a direction-checked upper float
conversion. This step cannot lower the analytic ceiling through roundoff.
It does not certify epsilon itself or the later statistical transcendental functions.

## Sources for arithmetic behavior

The implementation uses the standard-library exact rational conversion and
next-representable-float operations, not a new numerical-analysis method.

- Python fractions documentation: https://docs.python.org/3/library/fractions.html
- Python math.nextafter documentation: https://docs.python.org/3/library/math.html#math.nextafter

These official references were checked during the repair. High-precision tests
use mpmath as an independent numerical oracle, not as the proof of enclosure.
