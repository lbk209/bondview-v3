"""Elementary zero-coupon bond pricing using annual compounding."""

import math


def price_annual(face: float, annual_yield: float, years: float) -> float:
    """Price a zero-coupon payment with annual compounding.

    ``annual_yield`` is a "quoted annual effective yield, expressed as a
    decimal": 0.05 means 5% per year. ``years`` is time to payment in years.
    All inputs must be finite; face and years must be nonnegative, and
    annual_yield must be greater than -1. Invalid domains raise ValueError.
    """
    for name, value in (("face", face), ("annual_yield", annual_yield),
                        ("years", years)):
        if not math.isfinite(value):
            raise ValueError(f"{name} must be finite")
    if face < 0:
        raise ValueError("face must be nonnegative")
    if years < 0:
        raise ValueError("years must be nonnegative")
    if annual_yield <= -1:
        raise ValueError("annual_yield must be greater than -1")
    return face / (1 + annual_yield) ** years
