"""
validate_suite.py
=================

Complete validation and visualization suite for SSZ metric

© 2025 Carmen Wrede & Lino Casu
"""

import os
import argparse
import numpy as np
import matplotlib.pyplot as plt
from .constants import PHI, C, G, M_SUN, schwarzschild_radius
from .dilation import D_GR, D_SSZ
from .metric import A_blended, B_metric, natural_boundary
from .match_blend import find_intersection, verify_intersection

# UTF-8 fix for Windows
os.environ['PYTHONIOENCODING'] = 'utf-8:replace'

def validate_full_metric(M=M_SUN, varphi=PHI, show_plots=True, save_plots=True):
    """
    Complete validation of SSZ metric
    
    Parameters:
    -----------
    M : float
        Mass [kg] (default: Solar mass)
    varphi : float
        Golden ratio parameter (default: PHI)
    show_plots : bool
        Show interactive plots (default: True)
    save_plots : bool
        Save plots to docs/ (default: True)
    
    Returns:
    --------
    results : dict
        Validation results
    """
    print("="*80)
    print("SSZ FULL METRIC VALIDATION SUITE")
    print("="*80)
    
    # Setup
    rs = schwarzschild_radius(M)
    r_star, u_star = find_intersection(rs)
    r_phi = natural_boundary(rs)
    
    print(f"\nSystem parameters:")
    print(f"  Mass: M = {M:.3e} kg")
    print(f"  Schwarzschild radius: r_s = {rs/1000:.3f} km")
    print(f"  Intersection point: u* = {u_star:.10f}")
    print(f"  Intersection radius: r* = {r_star/rs:.6f} r_s")
    print(f"  Natural boundary: r_phi = {r_phi/rs:.6f} r_s")
    
    # Test range
    r_min = 0.85 * rs
    r_max = 10.0 * rs
    r = np.linspace(r_min, r_max, 800)
    
    # Compute time dilations
    D_gr = D_GR(r, rs)
    D_ssz = D_SSZ(r, rs)
    
    # Compute full metric
    A_full = np.array([A_blended(ri, rs, r_star) for ri in r])
    D_mix = np.sqrt(A_full)
    B_full = np.array([B_metric(ri, rs, r_star) for ri in r])
    
    # Validation checks
    print("\n" + "="*80)
    print("VALIDATION CHECKS")
    print("="*80)
    
    results = {}
    
    # Check 1: Intersection point accuracy
    verified, diff = verify_intersection(r_star, rs)
    results['intersection_verified'] = verified
    results['intersection_error'] = diff
    print(f"\n1. Intersection Point:")
    print(f"   u* = {u_star:.10f}")
    print(f"   Expected: ~1.386562")
    print(f"   Error: {abs(u_star - 1.386562):.2e}")
    if abs(u_star - 1.386562) < 1e-4:
        print("   ✓ PASS: Within 1e-4 of canonical value")
    else:
        print("   ✗ FAIL: Deviation too large")
    
    # Check 2: No signature flip (A > 0 everywhere)
    A_min = np.min(A_full)
    results['A_min'] = A_min
    results['no_signature_flip'] = A_min > 0
    print(f"\n2. No Signature Flip:")
    print(f"   min(A) = {A_min:.6f}")
    if A_min > 0:
        print("   ✓ PASS: A(r) > 0 everywhere")
    else:
        print("   ✗ FAIL: A(r) ≤ 0 detected!")
    
    # Check 3: A at natural boundary
    idx_phi = np.argmin(np.abs(r - r_phi))
    A_at_phi = A_full[idx_phi]
    results['A_at_r_phi'] = A_at_phi
    print(f"\n3. Natural Boundary:")
    print(f"   A(r_phi) = {A_at_phi:.6f}")
    if A_at_phi > 0:
        print("   ✓ PASS: Well-defined at r_phi")
    else:
        print("   ✗ FAIL: A(r_phi) ≤ 0")
    
    # Check 4: Far-field GR match
    r_far = r[-1]
    A_far = A_full[-1]
    D_gr_far = D_GR(r_far, rs)
    A_gr_far = D_gr_far**2
    far_field_error = abs(A_far - A_gr_far)
    results['far_field_error'] = far_field_error
    print(f"\n4. Far-Field GR Match:")
    print(f"   r = {r_far/rs:.1f} r_s")
    print(f"   A_SSZ = {A_far:.8f}")
    print(f"   A_GR = {A_gr_far:.8f}")
    print(f"   Error: {far_field_error:.2e}")
    if far_field_error < 1e-3:
        print("   ✓ PASS: Far-field matches GR")
    else:
        print("   ✗ FAIL: Far-field deviation")
    
    # Check 5: D_star matches at intersection
    idx_star = np.argmin(np.abs(r - r_star))
    D_star = D_mix[idx_star]
    results['D_star'] = D_star
    print(f"\n5. Time Dilation at r*:")
    print(f"   D* = {D_star:.8f}")
    print(f"   Expected: ~0.528")
    if 0.50 < D_star < 0.56:
        print("   ✓ PASS: D* in expected range")
    else:
        print("   ✗ FAIL: D* outside range")
    
    # Check 6: B = 1/A
    AB_product = A_full * B_full
    AB_error = np.max(np.abs(AB_product - 1.0))
    results['B_inverse_A_error'] = AB_error
    print(f"\n6. B = 1/A Relation:")
    print(f"   max|A·B - 1| = {AB_error:.2e}")
    if AB_error < 1e-10:
        print("   ✓ PASS: B = 1/A accurately")
    else:
        print("   ✗ FAIL: B ≠ 1/A")
    
    # Summary
    print("\n" + "="*80)
    print("VALIDATION SUMMARY")
    print("="*80)
    passed = sum([
        results['intersection_verified'],
        results['no_signature_flip'],
        results['A_at_r_phi'] > 0,
        results['far_field_error'] < 1e-3,
        0.50 < results['D_star'] < 0.56,
        results['B_inverse_A_error'] < 1e-10
    ])
    total = 6
    print(f"\nPassed: {passed}/{total} checks")
    print(f"Success rate: {passed/total*100:.1f}%")
    
    if passed == total:
        print("\n✓✓✓ ALL CHECKS PASSED! METRIC VALIDATED! ✓✓✓")
    else:
        print(f"\n⚠ {total-passed} check(s) failed")
    
    # Plots
    if show_plots or save_plots:
        print("\n" + "="*80)
        print("GENERATING PLOTS")
        print("="*80)
        
        fig = plt.figure(figsize=(16, 10))
        gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
        
        # Plot 1: Time dilation comparison
        ax1 = fig.add_subplot(gs[0, :2])
        ax1.plot(r/rs, D_gr, label='D_GR', linewidth=2, alpha=0.7)
        ax1.plot(r/rs, D_ssz, label='D_SSZ', linewidth=2, alpha=0.7)
        ax1.plot(r/rs, D_mix, label='D_mixed', linewidth=2.5, color='red')
        ax1.axvline(r_star/rs, ls=':', lw=1.5, color='blue', alpha=0.5, label=f'r* = {u_star:.3f}r_s')
        ax1.axvline(r_phi/rs, ls=':', lw=1.5, color='purple', alpha=0.5, label=f'r_phi = {r_phi/rs:.3f}r_s')
        ax1.set_xlabel('r/r_s', fontsize=11)
        ax1.set_ylabel('D(r)', fontsize=11)
        ax1.set_title('Time Dilation Comparison', fontsize=12, fontweight='bold')
        ax1.legend(fontsize=9)
        ax1.grid(True, alpha=0.3)
        ax1.set_xlim(r_min/rs, r_max/rs)
        
        # Plot 2: A(r) metric coefficient
        ax2 = fig.add_subplot(gs[0, 2])
        ax2.plot(r/rs, A_full, label='A_safe', linewidth=2, color='red')
        ax2.axvline(r_star/rs, ls=':', lw=1.5, color='blue', alpha=0.5)
        ax2.axvline(r_phi/rs, ls=':', lw=1.5, color='purple', alpha=0.5)
        ax2.axhline(0, color='gray', linestyle='-', alpha=0.3)
        ax2.set_xlabel('r/r_s', fontsize=11)
        ax2.set_ylabel('A(r)', fontsize=11)
        ax2.set_title('Metric A(r)', fontsize=12, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        ax2.set_xlim(r_min/rs, r_max/rs)
        
        # Plot 3: Near boundary detail
        r_near = np.linspace(0.8*rs, 2*rs, 400)
        A_near = np.array([A_blended(ri, rs, r_star) for ri in r_near])
        
        ax3 = fig.add_subplot(gs[1, 0])
        ax3.plot(r_near/rs, A_near, linewidth=2, color='red')
        ax3.axvline(r_star/rs, ls=':', lw=1.5, color='blue', alpha=0.5, label='r*')
        ax3.axvline(r_phi/rs, ls=':', lw=1.5, color='purple', alpha=0.5, label='r_phi')
        ax3.axhline(0, color='gray', linestyle='-', alpha=0.3)
        ax3.set_xlabel('r/r_s', fontsize=11)
        ax3.set_ylabel('A(r)', fontsize=11)
        ax3.set_title('Near Boundary Detail', fontsize=12, fontweight='bold')
        ax3.legend(fontsize=9)
        ax3.grid(True, alpha=0.3)
        ax3.set_xlim(0.8, 2.0)
        
        # Plot 4: B(r) coefficient
        ax4 = fig.add_subplot(gs[1, 1])
        ax4.plot(r/rs, B_full, linewidth=2, color='green')
        ax4.axvline(r_star/rs, ls=':', lw=1.5, color='blue', alpha=0.5)
        ax4.axvline(r_phi/rs, ls=':', lw=1.5, color='purple', alpha=0.5)
        ax4.set_xlabel('r/r_s', fontsize=11)
        ax4.set_ylabel('B(r)', fontsize=11)
        ax4.set_title('Radial Metric B(r)', fontsize=12, fontweight='bold')
        ax4.grid(True, alpha=0.3)
        ax4.set_xlim(r_min/rs, r_max/rs)
        
        # Plot 5: A·B product
        ax5 = fig.add_subplot(gs[1, 2])
        ax5.plot(r/rs, AB_product, linewidth=2, color='orange')
        ax5.axhline(1.0, color='gray', linestyle='--', alpha=0.5)
        ax5.axvline(r_star/rs, ls=':', lw=1.5, color='blue', alpha=0.5)
        ax5.set_xlabel('r/r_s', fontsize=11)
        ax5.set_ylabel('A(r)·B(r)', fontsize=11)
        ax5.set_title('A·B Product Check', fontsize=12, fontweight='bold')
        ax5.grid(True, alpha=0.3)
        ax5.set_xlim(r_min/rs, r_max/rs)
        
        # Plot 6: Difference from GR
        D_diff = np.abs(D_mix - D_gr) / D_gr * 100  # percent
        
        ax6 = fig.add_subplot(gs[2, :])
        ax6.semilogy(r/rs, D_diff, linewidth=2, color='purple')
        ax6.axvline(r_star/rs, ls=':', lw=1.5, color='blue', alpha=0.5, label='r*')
        ax6.axvline(r_phi/rs, ls=':', lw=1.5, color='purple', alpha=0.5, label='r_phi')
        ax6.set_xlabel('r/r_s', fontsize=11)
        ax6.set_ylabel('|D_SSZ - D_GR|/D_GR (%)', fontsize=11)
        ax6.set_title('Relative Difference from GR', fontsize=12, fontweight='bold')
        ax6.legend(fontsize=9)
        ax6.grid(True, alpha=0.3, which='both')
        ax6.set_xlim(r_min/rs, r_max/rs)
        
        if save_plots:
            plt.savefig('docs/ssz_full_validation.png', dpi=150, bbox_inches='tight')
            print("\n✓ Plot saved: docs/ssz_full_validation.png")
        
        if show_plots:
            plt.show()
        else:
            plt.close()
    
    print("\n" + "="*80)
    print("VALIDATION COMPLETE")
    print("="*80)
    
    return results

def main():
    """Command-line interface"""
    parser = argparse.ArgumentParser(description='SSZ Full Metric Validation Suite')
    parser.add_argument('--rs', type=float, default=None, help='Schwarzschild radius [m]')
    parser.add_argument('--mass', type=float, default=M_SUN, help='Mass [kg]')
    parser.add_argument('--varphi', type=float, default=PHI, help='Golden ratio parameter')
    parser.add_argument('--no-plots', action='store_true', help='Skip interactive plots')
    parser.add_argument('--no-save', action='store_true', help='Skip saving plots')
    
    args = parser.parse_args()
    
    M = args.mass
    if args.rs is not None:
        # Compute mass from given r_s
        M = args.rs * C**2 / (2 * G)
    
    results = validate_full_metric(
        M=M,
        varphi=args.varphi,
        show_plots=not args.no_plots,
        save_plots=not args.no_save
    )
    
    return results

if __name__ == "__main__":
    main()
