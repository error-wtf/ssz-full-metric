"""
test_intersection.py
====================

Test intersection point calculation

© 2025 Carmen Wrede & Lino Casu
"""

import sys
sys.path.insert(0, 'E:\\ssz-full-metric-perfected')

from ssz_metric import find_intersection, verify_intersection, M_SUN, schwarzschild_radius

def test_intersection_canonical():
    """Test that u* ≈ 1.38656 (canonical value)"""
    r_s = schwarzschild_radius(M_SUN)
    r_star, u_star = find_intersection(r_s)
    
    print("="*80)
    print("INTERSECTION POINT TEST")
    print("="*80)
    print(f"\nSchwarzschild radius: r_s = {r_s:.3f} m")
    print(f"Intersection point:   u* = {u_star:.10f}")
    print(f"Intersection radius:  r* = {r_star:.3f} m = {r_star/r_s:.6f} r_s")
    
    # Check against canonical value
    u_canonical = 1.386562
    error = abs(u_star - u_canonical)
    
    print(f"\nCanonical value:      u_canonical = {u_canonical:.6f}")
    print(f"Error:                |u* - u_canonical| = {error:.2e}")
    
    assert error < 1e-4, f"u* deviates from canonical value by {error:.2e}"
    print("\n✅ PASSED: u* within 1e-4 of canonical value")
    
    # Verify intersection
    verified, diff = verify_intersection(r_star, r_s)
    print(f"\nVerification: |D_SSZ - D_GR| = {diff:.2e}")
    
    assert verified, f"Intersection not verified: diff = {diff:.2e}"
    print("✅ PASSED: D_SSZ = D_GR at r*")
    
    print("="*80)

if __name__ == "__main__":
    test_intersection_canonical()
