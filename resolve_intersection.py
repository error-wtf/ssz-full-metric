"""
resolve_intersection.py
========================

Resolve the discrepancy between two intersection calculations:
1. intersection_time_dilation.py: u* = 1.469
2. MATHEMATICAL_FORMULAS.md:      u* = 1.387

This script will:
- Calculate intersection with highest precision
- Verify both formula implementations
- Determine the correct value
- Document the result

© 2025 Carmen Wrede & Lino Casu
Licensed under the ANTI-CAPITALIST SOFTWARE LICENSE v1.4
"""

import os
import sys
import math
import numpy as np

# UTF-8 setup
os.environ['PYTHONIOENCODING'] = 'utf-8:replace'
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except:
        pass

# Try high-precision mpmath
try:
    import mpmath as mp
    HAS_MPMATH = True
    mp.dps = 50  # 50 decimal places
except ImportError:
    HAS_MPMATH = False

from scipy.optimize import brentq

# Golden ratio
PHI = (1 + math.sqrt(5)) / 2  # ≈ 1.618033988749894...


def D_GR(u):
    """GR time dilation: D = √(1 - 1/u)"""
    if u <= 1.0:
        return 0.0
    return math.sqrt(1.0 - 1.0/u)


def D_SSZ_formula1(u):
    """
    SSZ formula 1 (from intersection_time_dilation.py):
    D = 1 / (2 - exp(-φ·u))
    """
    return 1.0 / (2.0 - math.exp(-PHI * u))


def D_SSZ_formula2(u):
    """
    SSZ formula 2 (from MATHEMATICAL_FORMULAS.md):
    D = 1 / (1 + Ξ(u))
    where Ξ(u) = 1 - exp(-φ·u)
    
    This simplifies to:
    D = 1 / (2 - exp(-φ·u))
    
    SAME AS FORMULA 1! ✅
    """
    Xi = 1.0 - math.exp(-PHI * u)
    return 1.0 / (1.0 + Xi)


def find_intersection_scipy():
    """Find intersection using scipy (standard precision)."""
    def equation(u):
        return D_SSZ_formula1(u) - D_GR(u)
    
    u_star = brentq(equation, 1.01, 10.0)
    D_star = D_GR(u_star)
    
    return u_star, D_star


def find_intersection_mpmath():
    """Find intersection using mpmath (high precision)."""
    def equation(u):
        D_ssz = mp.mpf(1) / (mp.mpf(2) - mp.exp(-mp.mpf(PHI) * u))
        D_gr = mp.sqrt(mp.mpf(1) - mp.mpf(1)/u)
        return D_ssz - D_gr
    
    # Try multiple initial guesses
    for guess in [mp.mpf(1.2), mp.mpf(1.4), mp.mpf(1.5)]:
        try:
            u_star = mp.findroot(equation, guess)
            u_star_float = float(u_star)
            if u_star_float > 1.0:
                D_star = float(mp.sqrt(mp.mpf(1) - mp.mpf(1)/u_star))
                return u_star_float, D_star
        except:
            continue
    
    raise RuntimeError("Could not find intersection with mpmath")


def main():
    print("="*80)
    print("RESOLVING INTERSECTION DISCREPANCY")
    print("="*80)
    print()
    
    print("Golden Ratio φ:")
    print(f"  φ = {PHI:.15f}")
    print(f"  1/φ = {1/PHI:.15f}")
    print(f"  φ² = {PHI**2:.15f}")
    print(f"  φ² - φ - 1 = {PHI**2 - PHI - 1:.2e} (should be 0)")
    print()
    
    # Verify both formulas are identical
    print("-"*80)
    print("VERIFYING FORMULA EQUIVALENCE")
    print("-"*80)
    test_points = [1.5, 2.0, 3.0, 5.0, 10.0]
    print(f"{'u':<8} {'Formula 1':<15} {'Formula 2':<15} {'Difference':<15}")
    print("-"*80)
    
    max_diff = 0.0
    for u in test_points:
        D1 = D_SSZ_formula1(u)
        D2 = D_SSZ_formula2(u)
        diff = abs(D1 - D2)
        max_diff = max(max_diff, diff)
        print(f"{u:<8.2f} {D1:<15.12f} {D2:<15.12f} {diff:<15.2e}")
    
    print()
    if max_diff < 1e-15:
        print(f"✅ Formulas are IDENTICAL (max diff = {max_diff:.2e})")
    else:
        print(f"⚠️ Formulas differ! (max diff = {max_diff:.2e})")
    print()
    
    # Calculate intersection with standard precision
    print("-"*80)
    print("INTERSECTION CALCULATION (STANDARD PRECISION)")
    print("-"*80)
    u_scipy, D_scipy = find_intersection_scipy()
    print(f"Using scipy.optimize.brentq:")
    print(f"  u* = {u_scipy:.15f}")
    print(f"  D* = {D_scipy:.15f}")
    print()
    
    # Verify
    D_ssz_check = D_SSZ_formula1(u_scipy)
    D_gr_check = D_GR(u_scipy)
    diff_check = abs(D_ssz_check - D_gr_check)
    print(f"Verification:")
    print(f"  D_SSZ(u*) = {D_ssz_check:.15f}")
    print(f"  D_GR(u*)  = {D_gr_check:.15f}")
    print(f"  Difference = {diff_check:.2e}")
    print()
    
    # Calculate with high precision if available
    if HAS_MPMATH:
        print("-"*80)
        print("INTERSECTION CALCULATION (HIGH PRECISION)")
        print("-"*80)
        print(f"Using mpmath with {mp.dps} decimal places:")
        u_mp, D_mp = find_intersection_mpmath()
        print(f"  u* = {u_mp:.15f}")
        print(f"  D* = {D_mp:.15f}")
        print()
        
        # Compare
        u_diff = abs(u_scipy - u_mp)
        D_diff = abs(D_scipy - D_mp)
        print(f"Comparison:")
        print(f"  Δu = {u_diff:.2e}")
        print(f"  ΔD = {D_diff:.2e}")
        print()
        
        if u_diff < 1e-10:
            print("✅ Standard and high precision agree!")
        else:
            print(f"⚠️ Precision difference detected")
        print()
    
    # Compare with documented values
    print("-"*80)
    print("COMPARISON WITH DOCUMENTED VALUES")
    print("-"*80)
    
    u_doc1 = 1.46897140556343  # From intersection_time_dilation.py
    D_doc1 = 0.565023499563574
    
    u_doc2 = 1.386562  # From MATHEMATICAL_FORMULAS.md
    D_doc2 = 0.528007
    
    print(f"{'Source':<40} {'u*':<20} {'D*':<20}")
    print("-"*80)
    print(f"{'intersection_time_dilation.py':<40} {u_doc1:<20.15f} {D_doc1:<20.15f}")
    print(f"{'MATHEMATICAL_FORMULAS.md':<40} {u_doc2:<20.10f} {D_doc2:<20.10f}")
    print(f"{'This calculation (scipy)':<40} {u_scipy:<20.15f} {D_scipy:<20.15f}")
    if HAS_MPMATH:
        print(f"{'This calculation (mpmath)':<40} {u_mp:<20.15f} {D_mp:<20.15f}")
    print()
    
    # Determine which is correct
    diff1 = abs(u_scipy - u_doc1)
    diff2 = abs(u_scipy - u_doc2)
    
    print(f"Difference from doc1: {diff1:.2e}")
    print(f"Difference from doc2: {diff2:.2e}")
    print()
    
    if diff1 < diff2:
        print("✅ RESULT: intersection_time_dilation.py is CORRECT!")
        print(f"   u* = {u_doc1:.10f}")
        print(f"   D* = {D_doc1:.10f}")
        print()
        print("❌ MATHEMATICAL_FORMULAS.md has TYPO or uses different formula")
        print(f"   Documented: u* = {u_doc2}")
        print(f"   Should be:  u* = {u_scipy:.6f}")
    else:
        print("⚠️ MATHEMATICAL_FORMULAS.md value closer?")
        print("   Need to investigate formula difference")
    
    print()
    print("="*80)
    print("CANONICAL VALUES (FOR REFERENCE)")
    print("="*80)
    print()
    print(f"u* = {u_scipy:.10f} (r* = {u_scipy:.10f} × r_s)")
    print(f"D* = {D_scipy:.10f}")
    print()
    print("Physical meaning:")
    print(f"  At r = {u_scipy:.3f}r_s:")
    print(f"    - SSZ and GR time dilations are EQUAL")
    print(f"    - Both predict D = {D_scipy:.6f}")
    print(f"    - This is the crossover point!")
    print()
    
    # Physical distances for reference
    print("For common objects:")
    M_sun = 1.98847e30  # kg
    G = 6.67430e-11
    c = 2.99792458e8
    r_s_sun = 2*G*M_sun/c**2
    print(f"  Sun: r* = {u_scipy * r_s_sun/1000:.3f} km")
    
    M_sgr_a = 4.3e6 * M_sun
    r_s_sgr = 2*G*M_sgr_a/c**2
    print(f"  Sgr A*: r* = {u_scipy * r_s_sgr/1e6:.3f} million km")
    
    print()
    print("="*80)


if __name__ == "__main__":
    main()
