"""Stable photon support values with exact-rational outward enclosures.

The enclosure is for the supplied binary64 transmissions and penalty, not for
uncertain laboratory parameters. Nominal rates/preparations are decimal-evaluated
approximations. See docs/NUMERICAL_CONTRACT.md for the accepted numeric domain.
This module uses only the Python standard library; it does not certify the
classical exponential bound, statistical logarithm, or the entire experiment.
"""
from __future__ import annotations
from decimal import Decimal, localcontext, ROUND_HALF_EVEN
from fractions import Fraction
from functools import lru_cache
import math
import struct
import sys

MIN_TRANSMISSION = 1e-12
MAX_PENALTY = 1e18
MAX_MODES = 64


class PhotonNumericalDomainError(ValueError):
    """The numerical implementation does not accept this otherwise possible model."""


def accepted_inputs(eta, penalty):
    """Return immutable binary64 inputs; never clip an unsupported model."""
    if sys.float_info.radix != 2 or sys.float_info.mant_dig != 53:
        raise PhotonNumericalDomainError('IEEE-754 binary64 Python floats required')
    try:
        values = tuple(float(x) for x in eta)
        lam = float(penalty)
    except (TypeError, ValueError, OverflowError) as exc:
        raise PhotonNumericalDomainError('Finite scalar transmissions/penalty required') from exc
    if not 2 <= len(values) <= MAX_MODES:
        raise PhotonNumericalDomainError(f'Photon numeric domain: 2 <= modes <= {MAX_MODES}')
    if any(not math.isfinite(x) or not MIN_TRANSMISSION <= x <= 1 for x in values):
        raise PhotonNumericalDomainError('Photon numeric domain: 1e-12 <= each transmission <= 1')
    if not math.isfinite(lam) or not 0 <= lam <= MAX_PENALTY:
        raise PhotonNumericalDomainError('Photon numeric domain: 0 <= penalty <= 1e18')
    return values, lam


def outward_float(value: Fraction, upper: bool) -> float:
    """Convert a rational to a float and check the requested direction exactly."""
    result = float(value)
    if not math.isfinite(result):
        raise ArithmeticError('Nonfinite endpoint conversion')
    if (Fraction(result) < value) if upper else (Fraction(result) > value):
        result = math.nextafter(result, math.inf if upper else -math.inf)
    if (Fraction(result) < value) if upper else (Fraction(result) > value):
        raise ArithmeticError('Endpoint conversion did not enclose the rational')
    return result


def _bits(x: float) -> int:
    return struct.unpack('>Q', struct.pack('>d', x))[0]


def _float(bits: int) -> float:
    return struct.unpack('>d', struct.pack('>Q', bits))[0]


def secular_residual(beta: Fraction, eta: tuple[Fraction, ...], lam: Fraction) -> Fraction:
    """Exact monotone residual, algebraically equal to the original secular law.

    g(beta)=sum_i beta/(s*eta_i+u*beta)-m, u=1/(1+lam), s=1-u.
    Unlike subtraction of large eigenvalues this remains well scaled as lam grows.
    """
    u = 1 / (1 + lam)
    s = 1 - u
    return sum((beta / (s*x + u*beta) for x in eta), Fraction()) - len(eta)


@lru_cache(maxsize=2048)
def _enclosure(eta: tuple[float, ...], penalty: float):
    """All endpoint signs are evaluated by integer rational arithmetic."""
    e = tuple(Fraction(x) for x in eta)
    m = len(e)
    requested = Fraction(penalty)
    threshold = Fraction(1, m-1)
    lam = max(requested, threshold)
    harmonic = Fraction(m) / sum((1/x for x in e), Fraction())
    lo = outward_float(harmonic, False)
    hi = max(eta)
    if secular_residual(Fraction(lo), e, lam) > 0:
        raise ArithmeticError('Harmonic lower bracket failed')
    if secular_residual(Fraction(hi), e, lam) < 0:
        raise ArithmeticError('Maximum-transmission upper bracket failed')
    # The positive binary64 bit ordering is monotone. Integer bisection needs at
    # most 63 steps and terminates at adjacent floats, independent of conditioning.
    il, ih = _bits(lo), _bits(hi)
    while ih-il > 1:
        mid = (il+ih)//2
        sign = secular_residual(Fraction(_float(mid)), e, lam)
        if sign == 0:
            il = ih = mid
            break
        if sign < 0:
            il = mid
        else:
            ih = mid
    blo, bhi = Fraction(_float(il)), Fraction(_float(ih))
    if not secular_residual(blo, e, lam) <= 0 <= secular_residual(bhi, e, lam):
        raise ArithmeticError('Final exact secular signs failed')
    lower, upper = blo, bhi
    if requested < threshold:
        # P_ME=(1+(m-1)*beta_at_threshold)/m. This affine transformation is
        # exact even when the usual floating representation of 1/(m-1) is low.
        lower = (1+requested)*(1+(m-1)*blo)/m-requested
        upper = (1+requested)*(1+(m-1)*bhi)/m-requested
    return outward_float(lower, False), outward_float(upper, True), blo, bhi, lam


def support_interval(eta, penalty) -> dict:
    """Enclose the optimum over the stated photon architecture, not a candidate score."""
    e, penalty = accepted_inputs(eta, penalty)
    lo, hi, blo, bhi, lam = _enclosure(e, penalty)
    return {'lower': lo, 'upper': hi,
            'branch_lower': float(blo), 'branch_upper': float(bhi),
            'effective_penalty_ratio': (lam.numerator, lam.denominator),
            'method': 'exact_rational_secular_signs_outward_binary64',
            'input_convention': 'exact values of supplied binary64 numbers'}


def stable_solution(eta, penalty) -> dict:
    """Nominal attaining recipe plus a separately certified support enclosure.

    At the float representation of the branch threshold retain inconclusive
    vacuum, as in the historical API. Its score differs from the exact binary64
    optimum by at most rounding scale; the enclosure always uses the exact
    rational threshold. Rates and preparations are not interval certificates.
    """
    e, penalty = accepted_inputs(eta, penalty)
    low, high, blo, bhi, lam = _enclosure(e, penalty)
    m = len(e)
    with localcontext() as ctx:
        ctx.prec = 90
        ctx.rounding = ROUND_HALF_EVEN
        def dec(q):
            q = Fraction(q)
            return Decimal(q.numerator) / Decimal(q.denominator)
        b = dec((blo+bhi)/2)
        ell = dec(lam)
        ed = [Decimal.from_float(x) for x in e]
        u = 1/(1+ell)
        s = 1-u
        weights = [x/(u*b+s*x)**2 for x in ed]
        norm = sum(weights)
        p = [x/norm for x in weights]
        amplitudes = [(x*y).sqrt() for x,y in zip(ed,p)]
        mean = sum(amplitudes)/m
        correct = m*mean**2
        # Nonnegative variance identity; no survival-minus-correct cancellation.
        error = sum((x-mean)**2 for x in amplitudes)
        failure = 1-sum(x*y for x,y in zip(ed,p))
        if penalty < 1/(m-1):
            correct += failure/m
            error += (m-1)*failure/m
            failure = Decimal(0)
        score_rates = correct-Decimal.from_float(penalty)*error
        score = float((Fraction(low)+Fraction(high))/2)
        if abs(float(score_rates)-score) > 2e-12:
            raise ArithmeticError('Nominal recipe and enclosed support disagree')
        return {'C':float(correct),'E':float(error),'F':float(failure),
                'p':tuple(float(x) for x in p),'score':score,
                'score_lower':low,'score_upper':high,
                'eigenvalue':float((blo+bhi)/2),'effective_penalty':float(lam)}


def reverse_support_upper(eta, penalty: float, operator_radius: float) -> tuple[float,float]:
    """Outward-safe support plus the proved trace-distance perturbation allowance."""
    bounds = support_interval(eta, penalty)
    radius = float(operator_radius)
    if not math.isfinite(radius) or radius < 0:
        raise ValueError('operator_radius must be finite and nonnegative')
    total = Fraction(bounds['upper']) + 2*(1+Fraction(float(penalty)))*Fraction(radius)
    return bounds['upper'], outward_float(min(Fraction(1), total), True)
