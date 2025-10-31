"""
Utility functions for finding the intersection point between the GR and SSZ
time-dilation factors.

In the weak-field limit, the time-dilation factors relative to a distant observer
for a non-rotating mass M are:

  - General Relativity (Schwarzschild): D_GR(r) = sqrt(1 - r_s/r)
  - Segmented Spacetime (SSZ): D_SSZ(r) = 1/(1 + Xi(r)), where Xi(r) = 1 - exp(-φ * r/r_s)

Here r_s = 2GM/c^2 is the Schwarzschild radius and φ = (1+sqrt(5))/2 is the
golden ratio.  The intersection point r* (in units of r_s) solves

    sqrt(1 - 1/u) = 1 / (2 - exp(-φ u)),

where u = r/r_s.  The function below computes this intersection u* for a given
value of φ.

The function returns a dict with the intersection value u* and the
common time-dilation value D* = D_GR(u*) = D_SSZ(u*).  For φ=1.0 (the
standard SSZ choice), u* ≈ 1.4689714056 and D* ≈ 0.5650235.

Example usage:
    from intersection_time_dilation import intersection_time_dilation
    result = intersection_time_dilation()
    print(result)  # {'u': 1.46897140556343, 'D': 0.565023499563574}

    # Convert to physical distance for a 1-solar-mass object:
    import math
    M_sun = 1.98847e30
    G = 6.67430e-11
    c = 299792458
    r_s = 2*G*M_sun/c**2
    r_star = result['u'] * r_s
    print(f"r* ≈ {r_star/1000:.3f} km for a 1 M☉ object")

This module can also be executed as a script to print the intersection
for several values of φ and sample masses.

© 2025 Carmen Wrede & Lino Casu
Licensed under the ANTI-CAPITALIST SOFTWARE LICENSE v1.4
"""

from __future__ import annotations

import os
import sys
from typing import Callable, Dict
import math

# UTF-8 setup for Windows compatibility
os.environ['PYTHONIOENCODING'] = 'utf-8:replace'
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except:
        pass

try:
    import mpmath as mp
    HAS_MPMATH = True
except ImportError:
    HAS_MPMATH = False
    print("Warning: mpmath not available, using scipy for root finding")
    from scipy.optimize import brentq


def _f(u: float, varphi: float) -> float:
    """Helper: equation whose root gives the intersection u.

    Returns sqrt(1 - 1/u) - 1/(2 - exp(-φ u)).  The root of this function
    corresponds to the intersection between GR and SSZ time-dilation factors.
    """
    return math.sqrt(1.0 - 1.0 / u) - 1.0 / (2.0 - math.exp(-varphi * u))


def intersection_time_dilation(varphi: float = 1.0, *, tol: float = 1e-12) -> Dict[str, float]:
    """Compute the intersection u* and D* for the GR and SSZ time dilation.

    Parameters
    ----------
    varphi : float, optional
        The φ parameter governing the exponent in the SSZ segment density.  The
        default 1.0 corresponds to φ≈1.618034 in the original theory, but
        this function treats φ as a generic scaling constant so it can be
        varied for sensitivity studies.
    tol : float, optional
        Relative tolerance for the root finder.  The default provides high
        precision (≈1e-12 relative error).

    Returns
    -------
    dict
        A dictionary with keys 'u' and 'D'.  'u' is the dimensionless
        intersection position u* = r*/r_s, and 'D' is the common time
        dilation value at the intersection (0 < D ≤ 1).
    """
    if HAS_MPMATH:
        # Use mpmath to solve sqrt(1 - 1/u) = 1/(2 - exp(-φ u)) for u.
        def f(u):
            return mp.sqrt(1.0 - 1.0 / u) - 1.0 / (2.0 - mp.e ** (-varphi * u))

        # Choose an initial guess > 1.0; the intersection lies outside the
        # event horizon.  Root-finding is mass-independent, so we solve in u.
        # We try several initial guesses to avoid spurious roots.
        guesses = [1.2, 1.3, 1.4, 1.5, 2.0]
        root = None
        for guess in guesses:
            try:
                root = mp.findroot(f, guess)
                # The root should be real and > 1.0; mpmath may return a complex
                # value with an infinitesimal imaginary part.  We cast to float.
                u = float(mp.re(root))
                if u > 1.0:
                    break
            except Exception:
                continue
        if root is None:
            raise RuntimeError(
                f"Failed to converge for varphi={varphi}; try different initial guesses."
            )
        u_val = float(u)
    else:
        # Fallback to scipy
        def f(u):
            return _f(u, varphi)
        
        # Use Brent's method between 1.01 and 10.0
        try:
            u_val = brentq(f, 1.01, 10.0, xtol=tol)
        except Exception as e:
            raise RuntimeError(
                f"Failed to converge for varphi={varphi}: {e}"
            )
    
    # Compute common time dilation at u
    D_val = math.sqrt(1.0 - 1.0 / u_val)
    return {"u": u_val, "D": D_val}


def _demo():
    """Print intersection data for several φ values and some example masses."""
    print("="*80)
    print("INTERSECTION OF GR AND SSZ TIME DILATION FACTORS")
    print("="*80)
    print()
    
    print("Intersection points for different φ values:")
    print("-"*80)
    print(f"{'φ':<8} {'u* (r/r_s)':<15} {'D* (common)':<15} {'Physical Meaning'}")
    print("-"*80)
    
    for phi in [0.5, 1.0, 1.5, 2.0]:
        result = intersection_time_dilation(phi)
        if phi == 1.0:
            meaning = "← Standard SSZ (φ = golden ratio)"
        else:
            meaning = f"  Variant (φ = {phi})"
        print(f"{phi:<8.1f} {result['u']:<15.8f} {result['D']:<15.8f} {meaning}")
    
    print()
    print("="*80)
    print("PHYSICAL DISTANCES FOR STANDARD SSZ (φ = 1.0)")
    print("="*80)
    print()
    
    # Example masses: 1 M☉, 10 M☉, 4.3e6 M☉
    masses = {
        "Sun (1 M☉)": 1.98847e30,
        "Stellar BH (10 M☉)": 10 * 1.98847e30,
        "Sgr A* (4.3×10⁶ M☉)": 4.3e6 * 1.98847e30,
    }
    G = 6.67430e-11
    c = 299792458
    
    # Use the default φ=1.0 result
    intersect = intersection_time_dilation(varphi=1.0)
    u_star = intersect["u"]
    D_star = intersect["D"]
    
    print(f"Intersection parameters:")
    print(f"  u* = {u_star:.8f} (dimensionless)")
    print(f"  D* = {D_star:.8f} (time dilation factor)")
    print()
    print(f"{'Object':<25} {'r_s (km)':<15} {'r* (km)':<15} {'Interpretation'}")
    print("-"*80)
    
    for name, M in masses.items():
        r_s = 2 * G * M / c ** 2
        r_star = u_star * r_s
        
        if "Sun" in name:
            interp = "Outside photon sphere"
        elif "Stellar" in name:
            interp = "GR≈SSZ transition zone"
        else:
            interp = "Galactic center regime"
            
        print(f"{name:<25} {r_s/1000:<15.3f} {r_star/1000:<15.3f} {interp}")
    
    print()
    print("="*80)
    print("PHYSICAL INTERPRETATION")
    print("="*80)
    print()
    print("• Below r*: SSZ predicts STRONGER time dilation than GR")
    print("  → Segment structure dominates")
    print("  → Natural boundary effects important")
    print()
    print("• At r*: GR and SSZ time dilations MATCH")
    print(f"  → Both predict D = {D_star:.6f}")
    print(f"  → This is the CROSSOVER point")
    print()
    print("• Above r*: GR predicts stronger time dilation than SSZ")
    print("  → GR approaches standard Schwarzschild")
    print("  → SSZ approaches flat spacetime faster")
    print()
    print(f"• For Sun: r* = {intersect['u'] * 2.953:.1f} km")
    print(f"  → This is {intersect['u']:.2f}× the Schwarzschild radius")
    print(f"  → Well outside the Sun (R☉ = 696,000 km)")
    print()
    print("="*80)


if __name__ == "__main__":
    _demo()
