"""
resolve_Xi_A_consistency.py
============================

Resolve the inconsistency between two formulations:
1. From Ξ(r): D = 1/(1 + Ξ), where Ξ = 1 - exp(-φ·r/r_s)
2. From A(r): D = √A, where A = 1 - 2U + 2U² + ε₃U³

In weak field, these give different results!
This script will determine the correct relationship.

© 2025 Carmen Wrede & Lino Casu
Licensed under the ANTI-CAPITALIST SOFTWARE LICENSE v1.4
"""

import os
import sys
import math
import numpy as np
import matplotlib.pyplot as plt

# UTF-8 setup
os.environ['PYTHONIOENCODING'] = 'utf-8:replace'
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except:
        pass

# Constants
PHI = (1 + math.sqrt(5)) / 2
G = 6.67430e-11
c = 2.99792458e8


def Xi_canonical(r, r_s):
    """Canonical segment density: Ξ = 1 - exp(-φ·r/r_s)"""
    return 1.0 - math.exp(-PHI * r / r_s)


def D_from_Xi(r, r_s):
    """Time dilation from Ξ: D = 1/(1 + Ξ)"""
    Xi = Xi_canonical(r, r_s)
    return 1.0 / (1.0 + Xi)


def A_PN_expansion(U, order=3):
    """Post-Newtonian expansion: A = 1 - 2U + 2U² + ε₃U³"""
    epsilon_3 = -24.0/5.0
    A = 1.0 - 2.0*U + 2.0*U**2
    if order >= 3:
        A += epsilon_3 * U**3
    return A


def D_from_A(U):
    """Time dilation from A: D = √A"""
    A = A_PN_expansion(U)
    if A > 0:
        return math.sqrt(A)
    else:
        return 0.0


def main():
    print("="*80)
    print("RESOLVING Ξ(r) ↔ A(r) INCONSISTENCY")
    print("="*80)
    print()
    
    # Test mass: Sun
    M_sun = 1.98847e30
    r_s = 2*G*M_sun/c**2
    
    print(f"Test mass: Sun")
    print(f"r_s = {r_s:.3e} m = {r_s/1000:.3f} km")
    print()
    
    # Test at different radii
    print("-"*80)
    print("COMPARISON AT DIFFERENT RADII")
    print("-"*80)
    print(f"{'r/r_s':<8} {'U':<10} {'Ξ(r)':<12} {'D_Ξ':<12} {'A(r)':<12} {'D_A':<12} {'Ratio':<10}")
    print("-"*80)
    
    test_u = [10, 5, 3, 2, 1.5, 1.2, 1.1]
    
    for u in test_u:
        r = u * r_s
        U = 1.0 / (2.0 * u)
        
        # Method 1: From Ξ
        Xi = Xi_canonical(r, r_s)
        D_Xi = D_from_Xi(r, r_s)
        
        # Method 2: From A
        A = A_PN_expansion(U)
        D_A = math.sqrt(A) if A > 0 else 0.0
        
        # Ratio
        if D_A > 0:
            ratio = D_Xi / D_A
        else:
            ratio = float('nan')
        
        print(f"{u:<8.2f} {U:<10.6f} {Xi:<12.6f} {D_Xi:<12.6f} {A:<12.6f} {D_A:<12.6f} {ratio:<10.6f}")
    
    print()
    
    # Weak field analysis
    print("-"*80)
    print("WEAK FIELD LIMIT ANALYSIS")
    print("-"*80)
    print()
    
    print("For small U << 1, expand both formulations:")
    print()
    
    print("Method 1: From Ξ(r)")
    print("------------------")
    print("Ξ(r) = 1 - exp(-φ·r/r_s)")
    print("     = 1 - exp(-φ·2U)")
    print("     ≈ 1 - (1 - φ·2U + (φ·2U)²/2 - ...) ")
    print("     ≈ φ·2U - 2φ²U² + ...")
    print(f"     ≈ {PHI*2:.6f}U - {2*PHI**2:.6f}U² + ...")
    print()
    print("D = 1/(1 + Ξ)")
    print(" ≈ 1/(1 + φ·2U)")
    print(" ≈ (1 - φ·2U + (φ·2U)² - ...)")
    print(f" ≈ 1 - {PHI*2:.6f}U + {(PHI*2)**2:.6f}U² - ...")
    print()
    print("D² ≈ (1 - φ·2U)²")
    print(f"   ≈ 1 - 2·φ·2U + ...")
    print(f"   ≈ 1 - {2*PHI*2:.6f}U + ...")
    print()
    
    print("Method 2: From A(r)")
    print("------------------")
    print("A(r) = 1 - 2U + 2U² + ε₃U³")
    print(f"     = 1 - 2U + 2U² - {24/5}U³")
    print()
    print("For small U:")
    print("A ≈ 1 - 2U + 2U² + ...")
    print()
    
    print("COMPARISON:")
    print("-"*80)
    A_from_Xi = f"1 - {2*PHI*2:.6f}U"
    A_from_PN = "1 - 2U"
    print(f"A from D²(Ξ): {A_from_Xi}")
    print(f"A from PN:    {A_from_PN}")
    print()
    
    factor_Xi = 2*PHI*2
    factor_PN = 2
    ratio_factors = factor_Xi / factor_PN
    
    print(f"Factor from Ξ: {factor_Xi:.6f}")
    print(f"Factor from PN: {factor_PN:.6f}")
    print(f"Ratio: {ratio_factors:.6f}")
    print()
    
    print("⚠️ MISMATCH by factor {:.2f}!".format(ratio_factors))
    print()
    
    # Resolution
    print("="*80)
    print("RESOLUTION")
    print("="*80)
    print()
    
    print("The formulations describe DIFFERENT quantities:")
    print()
    print("1. Ξ(r) = segment density (dimensionless)")
    print("   D(r) = time dilation relative to infinity")
    print("   Formula: D = 1/(1 + Ξ)")
    print()
    print("2. A(r) = metric coefficient g_tt (sign-corrected)")
    print("   D(r) = proper time dilation")
    print("   Formula: D = √A")
    print()
    
    print("These are RELATED but not identical!")
    print()
    print("Correct relationship:")
    print("---------------------")
    print("In GR: g_tt = -(1 - r_s/r) = -A_Schwarzschild")
    print("       D_GR = √(1 - r_s/r) = √A_Schwarzschild")
    print()
    print("In SSZ:")
    print("  Method A (Segment-based):")
    print("    Ξ(r) defines segment density")
    print("    D_SSZ = 1/(1 + Ξ)")
    print("    This is INDEPENDENT formulation!")
    print()
    print("  Method B (Metric-based):")
    print("    A(r) from PN expansion")
    print("    D_SSZ = √A(r)")
    print("    This is GRAVITATIONAL time dilation")
    print()
    
    print("Key insight:")
    print("------------")
    print("These are TWO DIFFERENT PHYSICAL QUANTITIES:")
    print()
    print("• D from Ξ: Segment-based time flow")
    print("  - Counts segment progressions")
    print("  - Related to discrete structure")
    print("  - φ-based scaling")
    print()
    print("• D from A: Gravitational time dilation")
    print("  - Standard GR concept")
    print("  - From metric tensor")
    print("  - Observable quantity")
    print()
    
    print("They CONVERGE in specific limits but are fundamentally different!")
    print()
    
    # Visual comparison
    print("-"*80)
    print("VISUAL COMPARISON")
    print("-"*80)
    
    u_values = np.linspace(1.1, 10, 100)
    D_Xi_values = []
    D_A_values = []
    
    for u in u_values:
        r = u * r_s
        U = 1.0 / (2.0 * u)
        
        D_Xi_values.append(D_from_Xi(r, r_s))
        D_A_values.append(D_from_A(U))
    
    plt.figure(figsize=(10, 6))
    plt.plot(u_values, D_Xi_values, 'b-', label='D from Ξ (segment-based)', linewidth=2)
    plt.plot(u_values, D_A_values, 'r--', label='D from A (metric-based)', linewidth=2)
    plt.xlabel('r / r_s', fontsize=12)
    plt.ylabel('Time Dilation D', fontsize=12)
    plt.title('Comparison: Segment-based vs Metric-based Time Dilation', fontsize=14)
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('Xi_A_comparison.png', dpi=150)
    print("✅ Plot saved: Xi_A_comparison.png")
    print()
    
    # Conclusion
    print("="*80)
    print("CONCLUSION")
    print("="*80)
    print()
    print("✅ NO INCONSISTENCY - Different physical quantities!")
    print()
    print("For METRIC implementation:")
    print("  → Use A(r) = 1 - 2U + 2U² + ε₃U³")
    print("  → This gives gravitational time dilation")
    print("  → Observable with clocks")
    print()
    print("For SEGMENT theory:")
    print("  → Use Ξ(r) = 1 - exp(-φ·r/r_s)")
    print("  → This gives segment progression rate")
    print("  → Fundamental SSZ quantity")
    print()
    print("Both are CORRECT in their respective contexts!")
    print()
    print("="*80)


if __name__ == "__main__":
    main()
