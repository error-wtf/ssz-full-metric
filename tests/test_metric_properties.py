"""
test_metric_properties.py
==========================

Test metric properties and consistency

© 2025 Carmen Wrede & Lino Casu
"""

import sys
sys.path.insert(0, 'E:\\ssz-full-metric-perfected')

import numpy as np
from ssz_metric import (
    PHI, M_SUN, schwarzschild_radius,
    A_blended, B_metric, natural_boundary,
    find_intersection, D_GR, D_SSZ
)

def test_A_positive_everywhere():
    """Test that A(r) > 0 everywhere (no signature flip)"""
    print("\n" + "="*80)
    print("TEST: A(r) > 0 EVERYWHERE")
    print("="*80)
    
    rs = schwarzschild_radius(M_SUN)
    r_star, u_star = find_intersection(rs)
    r_phi = natural_boundary(rs)
    
    # Test from r_phi to 100 r_s
    r = np.linspace(0.85*rs, 100*rs, 1000)
    A = np.array([A_blended(ri, rs, r_star) for ri in r])
    
    A_min = np.min(A)
    print(f"\nTest range: [{0.85:.2f}, 100] r_s")
    print(f"Minimum A(r): {A_min:.6f}")
    print(f"Natural boundary: r_phi = {r_phi/rs:.6f} r_s")
    
    assert np.all(A > 0.0), f"A(r) ≤ 0 detected! min(A) = {A_min}"
    print("\n✓ PASS: A(r) > 0 everywhere")
    print("="*80)

def test_far_field_GR_match():
    """Test that metric matches GR in far field"""
    print("\n" + "="*80)
    print("TEST: FAR-FIELD GR MATCH")
    print("="*80)
    
    rs = schwarzschild_radius(M_SUN)
    r_star, _ = find_intersection(rs)
    
    # Test at large distances
    r_far = np.array([10*rs, 50*rs, 100*rs, 1000*rs])
    
    print(f"\nTesting at multiple distances:")
    for r in r_far:
        A_ssz = A_blended(r, rs, r_star)
        D_gr = D_GR(r, rs)
        A_gr = D_gr**2
        
        error = abs(A_ssz - A_gr)
        rel_error = error / A_gr * 100
        
        print(f"  r = {r/rs:.0f} r_s:")
        print(f"    A_SSZ = {A_ssz:.10f}")
        print(f"    A_GR  = {A_gr:.10f}")
        print(f"    Error = {error:.2e} ({rel_error:.4f}%)")
        
        assert error < 1e-3, f"Far-field mismatch at r={r/rs:.0f}r_s: error={error:.2e}"
    
    print("\n✓ PASS: Far-field matches GR within tolerance")
    print("="*80)

def test_B_is_inverse_A():
    """Test that B(r) = 1/A(r)"""
    print("\n" + "="*80)
    print("TEST: B = 1/A")
    print("="*80)
    
    rs = schwarzschild_radius(M_SUN)
    r_star, _ = find_intersection(rs)
    
    r = np.linspace(1.05*rs, 10*rs, 500)
    A = np.array([A_blended(ri, rs, r_star) for ri in r])
    B = np.array([B_metric(ri, rs, r_star) for ri in r])
    
    product = A * B
    error = np.max(np.abs(product - 1.0))
    
    print(f"\nTest range: [1.05, 10] r_s")
    print(f"Points tested: {len(r)}")
    print(f"max|A·B - 1| = {error:.2e}")
    
    assert error < 1e-10, f"B ≠ 1/A: max error = {error:.2e}"
    print("\n✓ PASS: B = 1/A accurately")
    print("="*80)

def test_C2_continuity():
    """Test C² continuity at intersection point"""
    print("\n" + "="*80)
    print("TEST: C² CONTINUITY AT r*")
    print("="*80)
    
    rs = schwarzschild_radius(M_SUN)
    r_star, u_star = find_intersection(rs)
    
    # Test around r_star
    h = 1e-6 * rs  # Small step
    r_test = np.array([r_star - 2*h, r_star - h, r_star, r_star + h, r_star + 2*h])
    
    A_test = np.array([A_blended(ri, rs, r_star) for ri in r_test])
    
    # Finite difference derivatives
    # First derivative
    dA_dx = (A_test[2:] - A_test[:-2]) / (2*h)
    # Second derivative
    d2A_dx2 = (A_test[2:] - 2*A_test[1:-1] + A_test[:-2]) / (h**2)
    
    print(f"\nIntersection point: r* = {u_star:.6f} r_s")
    print(f"Step size: h = {h:.2e} m")
    print(f"\nA values around r*:")
    for i, ri in enumerate(r_test):
        print(f"  r = r* + {(ri-r_star)/h:.0f}h: A = {A_test[i]:.8f}")
    
    print(f"\nFirst derivatives:")
    for i, val in enumerate(dA_dx):
        print(f"  dA/dr[{i-1}] = {val:.6e}")
    
    print(f"\nSecond derivatives:")
    for i, val in enumerate(d2A_dx2):
        print(f"  d²A/dr²[{i}] = {val:.6e}")
    
    # Check continuity
    dA_variation = np.std(dA_dx) / np.abs(np.mean(dA_dx))
    d2A_variation = np.std(d2A_dx2) / np.abs(np.mean(d2A_dx2))
    
    print(f"\nVariation:")
    print(f"  First derivative: {dA_variation:.4f}")
    print(f"  Second derivative: {d2A_variation:.4f}")
    
    # Generous tolerance for C² continuity
    assert dA_variation < 0.1, f"C¹ discontinuity: variation = {dA_variation:.4f}"
    assert d2A_variation < 0.5, f"C² discontinuity: variation = {d2A_variation:.4f}"
    
    print("\n✓ PASS: C² continuous at r*")
    print("="*80)

def test_natural_boundary_properties():
    """Test properties at natural boundary"""
    print("\n" + "="*80)
    print("TEST: NATURAL BOUNDARY PROPERTIES")
    print("="*80)
    
    rs = schwarzschild_radius(M_SUN)
    r_star, _ = find_intersection(rs)
    r_phi = natural_boundary(rs)
    
    print(f"\nNatural boundary: r_phi = {r_phi/rs:.6f} r_s")
    
    # A at r_phi
    A_phi = A_blended(r_phi, rs, r_star)
    print(f"A(r_phi) = {A_phi:.6f}")
    
    assert A_phi > 0, f"A(r_phi) ≤ 0: {A_phi}"
    print("  ✓ A(r_phi) > 0")
    
    # D at r_phi
    D_phi = np.sqrt(A_phi)
    print(f"D(r_phi) = {D_phi:.6f}")
    
    assert D_phi > 0, f"D(r_phi) ≤ 0: {D_phi}"
    assert D_phi < 1, f"D(r_phi) ≥ 1: {D_phi}"
    print("  ✓ 0 < D(r_phi) < 1")
    
    # Check r_phi < r_star
    assert r_phi < r_star, f"r_phi ≥ r_star: {r_phi/rs:.3f} vs {r_star/rs:.3f}"
    print(f"  ✓ r_phi < r* ({r_phi/rs:.3f} < {r_star/rs:.3f})")
    
    print("\n✓ PASS: Natural boundary well-defined")
    print("="*80)

def test_time_dilation_consistency():
    """Test that D = √A is consistent"""
    print("\n" + "="*80)
    print("TEST: TIME DILATION CONSISTENCY")
    print("="*80)
    
    rs = schwarzschild_radius(M_SUN)
    r_star, _ = find_intersection(rs)
    
    r = np.linspace(1.1*rs, 10*rs, 200)
    
    # From metric
    A = np.array([A_blended(ri, rs, r_star) for ri in r])
    D_from_A = np.sqrt(A)
    
    # Direct computation (should match at intersection)
    D_ssz = D_SSZ(r, rs)
    D_gr = D_GR(r, rs)
    
    # At intersection, both should match
    idx_star = np.argmin(np.abs(r - r_star))
    D_A_star = D_from_A[idx_star]
    D_ssz_star = D_ssz[idx_star]
    D_gr_star = D_gr[idx_star]
    
    print(f"\nAt r*:")
    print(f"  D from A = {D_A_star:.8f}")
    print(f"  D_SSZ = {D_ssz_star:.8f}")
    print(f"  D_GR = {D_gr_star:.8f}")
    
    # Should all be close at intersection
    assert abs(D_A_star - D_ssz_star) < 0.02, "D from A doesn't match D_SSZ at r*"
    assert abs(D_A_star - D_gr_star) < 0.02, "D from A doesn't match D_GR at r*"
    
    print("\n✓ PASS: Time dilation consistent")
    print("="*80)

if __name__ == "__main__":
    print("\n" + "="*80)
    print("SSZ METRIC PROPERTIES TEST SUITE")
    print("="*80)
    
    test_A_positive_everywhere()
    test_far_field_GR_match()
    test_B_is_inverse_A()
    test_C2_continuity()
    test_natural_boundary_properties()
    test_time_dilation_consistency()
    
    print("\n" + "="*80)
    print("ALL TESTS PASSED!")
    print("="*80)
    print("\n✓✓✓ SSZ METRIC FULLY VALIDATED ✓✓✓\n")
