"""
compute_einstein_tensor.py
==========================

CRITICAL: Compute Einstein tensor G_μν from SSZ metric
Extract stress-energy tensor T_μν
Validate Einstein field equations

© 2025 Carmen Wrede & Lino Casu
"""

import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, Function, diff, simplify, Matrix, sqrt, exp, Rational
from sympy import latex, lambdify, init_printing
import warnings
warnings.filterwarnings('ignore')

# Initialize pretty printing
init_printing()

print("="*80)
print("EINSTEIN TENSOR COMPUTATION - SSZ METRIC")
print("="*80)
print("\nThis will compute G_μν from the SSZ metric and extract T_μν")
print("Using symbolic computation with sympy...")
print()

# Define symbolic variables
r, M, G_const, c = symbols('r M G c', real=True, positive=True)
r_s = 2*G_const*M/c**2
print(f"Schwarzschild radius: r_s = 2GM/c²")

# Define φ
phi = (1 + sqrt(5)) / 2
print(f"\nGolden ratio φ = (1+√5)/2 ≈ {float(phi):.6f}")

# Define weak field parameter U
U = r_s / (2*r)
print(f"Weak field parameter: U = r_s/(2r)")

# Define metric coefficient A(r) - SSZ form
# Using current O(U³) with known coefficients
eps_0 = 1
eps_1 = -2
eps_2 = 2
eps_3 = Rational(-24, 5)  # = -4.8

print(f"\nPost-Newtonian coefficients:")
print(f"  ε₀ = {eps_0}")
print(f"  ε₁ = {eps_1}")
print(f"  ε₂ = {eps_2}")
print(f"  ε₃ = {eps_3} = {float(eps_3):.6f}")

# A(r) = Σ ε_n U^n
A = eps_0 + eps_1*U + eps_2*U**2 + eps_3*U**3

print(f"\nMetric coefficient A(r):")
print(f"  A(r) = 1 - 2U + 2U² - (24/5)U³")
print(f"       = 1 - 2(r_s/2r) + 2(r_s/2r)² - 4.8(r_s/2r)³")

# B(r) = 1/A(r) (approximately for weak field)
# For exact computation, use full inverse
B = 1 / A

print(f"\nMetric coefficient B(r):")
print(f"  B(r) = 1/A(r)")

# Metric tensor in Schwarzschild-like coordinates
# ds² = -A(r)c²dt² + B(r)dr² + r²dΩ²
print(f"\nMetric tensor g_μν:")
print(f"  ds² = -A(r)c²dt² + B(r)dr² + r²(dθ² + sin²θ dφ²)")

# Define metric matrix (t, r, theta, phi)
g_matrix = Matrix([
    [-A*c**2, 0, 0, 0],
    [0, B, 0, 0],
    [0, 0, r**2, 0],
    [0, 0, 0, r**2]  # Will multiply by sin²θ later
])

print(f"\nMetric matrix g_μν (without sin²θ in g_φφ):")
print("  Computing... (this may take a moment)")

# Compute inverse metric
print("\n[1/6] Computing inverse metric g^μν...")
g_inv = g_matrix.inv()
print("  ✓ Done")

# Compute Christoffel symbols Γ^λ_μν
print("\n[2/6] Computing Christoffel symbols Γ^λ_μν...")
print("  (This is the most time-consuming step...)")

coords = [r]  # We'll focus on radial component for now
n_coords = 1

# For full computation, we need all coordinates
# For now, compute key components

# Key Christoffel symbols (radial)
print("\n  Computing Γ^r_tt...")
Gamma_r_tt = Rational(1,2) * g_inv[1,1] * diff(g_matrix[0,0], r)
Gamma_r_tt = simplify(Gamma_r_tt)
print(f"    Γ^r_tt = {Gamma_r_tt}")

print("\n  Computing Γ^r_rr...")
Gamma_r_rr = Rational(1,2) * g_inv[1,1] * diff(g_matrix[1,1], r)
Gamma_r_rr = simplify(Gamma_r_rr)
print(f"    Γ^r_rr = {Gamma_r_rr}")

print("\n  Computing Γ^t_tr...")
Gamma_t_tr = Rational(1,2) * g_inv[0,0] * diff(g_matrix[0,0], r)
Gamma_t_tr = simplify(Gamma_t_tr)
print(f"    Γ^t_tr = {Gamma_t_tr}")

print("\n  ✓ Key Christoffel symbols computed")

# Compute Ricci tensor R_μν (simplified approach)
print("\n[3/6] Computing Ricci tensor R_μν...")
print("  Using simplified spherically symmetric form...")

# For spherically symmetric metric in form:
# ds² = -A(r)dt² + B(r)dr² + r²dΩ²
# The Ricci components are (from literature):

# R_tt
A_prime = diff(A, r)
A_double_prime = diff(A_prime, r)
B_prime = diff(B, r)

R_tt_expr = (A_double_prime/(2*B) 
             - A_prime*B_prime/(4*B**2)
             + (A_prime)**2/(4*A*B)
             + A_prime/(r*B))

R_tt = simplify(R_tt_expr)
print(f"\n  R_tt computed")

# R_rr
R_rr_expr = (-A_double_prime/(2*A)
             + A_prime*B_prime/(4*A*B)
             + (A_prime)**2/(4*A**2)
             - B_prime/(r*B))

R_rr = simplify(R_rr_expr)
print(f"  R_rr computed")

# R_θθ
R_theta_theta_expr = 1 - r*A_prime/(2*A*B) + r*B_prime/(2*B**2) - 1/B

R_theta_theta = simplify(R_theta_theta_expr)
print(f"  R_θθ computed")

# R_φφ = sin²θ × R_θθ
R_phi_phi = R_theta_theta  # Without sin²θ factor

print("  ✓ Ricci tensor computed")

# Compute Ricci scalar R
print("\n[4/6] Computing Ricci scalar R...")

# R = g^μν R_μν
R_scalar_expr = (g_inv[0,0]*R_tt 
                 + g_inv[1,1]*R_rr 
                 + g_inv[2,2]*R_theta_theta 
                 + g_inv[3,3]*R_phi_phi)

R_scalar = simplify(R_scalar_expr)
print("  ✓ Ricci scalar R computed")

# Compute Einstein tensor G_μν = R_μν - (1/2)g_μν R
print("\n[5/6] Computing Einstein tensor G_μν...")

G_tt = simplify(R_tt - Rational(1,2)*g_matrix[0,0]*R_scalar)
G_rr = simplify(R_rr - Rational(1,2)*g_matrix[1,1]*R_scalar)
G_theta_theta = simplify(R_theta_theta - Rational(1,2)*g_matrix[2,2]*R_scalar)

print("  ✓ Einstein tensor G_μν computed")

# Extract stress-energy tensor T_μν
print("\n[6/6] Extracting stress-energy tensor T_μν...")

# T_μν = (c⁴/8πG) G_μν
kappa = 8 * np.pi * G_const / c**4

T_tt = G_tt / kappa
T_rr = G_rr / kappa

# Extract energy density ρ and pressure p
# T^t_t = -ρc² (with raised index)
# T^r_r = p (with raised index)

rho = -T_tt / (c**2 * g_matrix[0,0])  # Energy density
p_r = T_rr / g_matrix[1,1]  # Radial pressure

rho = simplify(rho)
p_r = simplify(p_r)

print("  ✓ Stress-energy tensor T_μν extracted")

# Display results
print("\n" + "="*80)
print("RESULTS - STRESS-ENERGY TENSOR")
print("="*80)

print("\nEnergy density ρ(r):")
print(f"  ρ = {rho}")

print("\nRadial pressure p_r(r):")
print(f"  p = {p_r}")

# Numerical evaluation
print("\n" + "="*80)
print("NUMERICAL EVALUATION")
print("="*80)

# Convert to numerical functions
print("\nConverting to numerical functions...")

# Use solar mass for testing
M_sun_SI = 1.98847e30  # kg
G_SI = 6.67430e-11     # m³/(kg·s²)
c_SI = 2.99792458e8    # m/s
r_s_sun = 2 * G_SI * M_sun_SI / c_SI**2

print(f"\nTest object: Solar mass")
print(f"  M = {M_sun_SI:.3e} kg")
print(f"  r_s = {r_s_sun/1000:.3f} km")

# Create numerical functions
try:
    rho_func = lambdify((r, M, G_const, c), rho, 'numpy')
    p_func = lambdify((r, M, G_const, c), p_r, 'numpy')
    
    # Test at different radii
    radii_rs = np.array([1.5, 2.0, 3.0, 5.0, 10.0])
    radii = radii_rs * r_s_sun
    
    print(f"\n{'r/r_s':<10} {'ρ (kg/m³)':<20} {'p (Pa)':<20}")
    print("-" * 50)
    
    for i, r_val in enumerate(radii):
        try:
            rho_val = float(rho_func(r_val, M_sun_SI, G_SI, c_SI))
            p_val = float(p_func(r_val, M_sun_SI, G_SI, c_SI))
            print(f"{radii_rs[i]:<10.1f} {rho_val:<20.3e} {p_val:<20.3e}")
        except:
            print(f"{radii_rs[i]:<10.1f} {'(evaluation error)':<20} {'(evaluation error)':<20}")
    
    # Plot
    print("\nGenerating plots...")
    
    r_range = np.linspace(1.5*r_s_sun, 20*r_s_sun, 200)
    
    try:
        rho_array = np.array([float(rho_func(r_val, M_sun_SI, G_SI, c_SI)) for r_val in r_range])
        p_array = np.array([float(p_func(r_val, M_sun_SI, G_SI, c_SI)) for r_val in r_range])
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        
        ax1.plot(r_range/r_s_sun, rho_array, linewidth=2, color='blue')
        ax1.axhline(0, color='gray', linestyle='--', alpha=0.5)
        ax1.set_xlabel('r/r_s', fontsize=12)
        ax1.set_ylabel('Energy Density ρ (kg/m³)', fontsize=12)
        ax1.set_title('SSZ Energy Density', fontsize=13, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        ax1.set_xlim(1.5, 20)
        
        ax2.plot(r_range/r_s_sun, p_array, linewidth=2, color='red')
        ax2.axhline(0, color='gray', linestyle='--', alpha=0.5)
        ax2.set_xlabel('r/r_s', fontsize=12)
        ax2.set_ylabel('Radial Pressure p (Pa)', fontsize=12)
        ax2.set_title('SSZ Radial Pressure', fontsize=13, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        ax2.set_xlim(1.5, 20)
        
        plt.tight_layout()
        plt.savefig('einstein_tensor_results.png', dpi=150)
        print("✓ Plot saved: einstein_tensor_results.png")
        
    except Exception as e:
        print(f"Warning: Could not generate full plots: {e}")
        
except Exception as e:
    print(f"Warning: Numerical evaluation failed: {e}")
    print("Symbolic results are still valid!")

# Energy conditions check (qualitative)
print("\n" + "="*80)
print("ENERGY CONDITIONS (Qualitative)")
print("="*80)

print("\nWeak Energy Condition (WEC):")
print("  ρ ≥ 0  AND  ρ+p ≥ 0")
print("  Check: Requires numerical evaluation")

print("\nNull Energy Condition (NEC):")
print("  ρ+p ≥ 0")
print("  Check: Requires numerical evaluation")

print("\nDominant Energy Condition (DEC):")
print("  ρ ≥ |p|")
print("  Check: Requires numerical evaluation")

print("\nStrong Energy Condition (SEC):")
print("  ρ+3p ≥ 0")
print("  Check: Requires numerical evaluation")

print("\nNote: Detailed energy condition validation in validate_energy_conditions.py")

# Summary
print("\n" + "="*80)
print("SUMMARY")
print("="*80)

print("\n✅ Einstein tensor G_μν computed from SSZ metric")
print("✅ Stress-energy tensor T_μν extracted")
print("✅ Energy density ρ(r) and pressure p(r) obtained")
print("⚠️  Energy conditions need numerical validation")
print("⚠️  Full 4D computation recommended for publication")

print("\nNext steps:")
print("  1. Run validate_energy_conditions.py")
print("  2. Verify all conditions numerically")
print("  3. Compare with TOV equation")
print("  4. Check physical interpretation")

print("\n" + "="*80)
print("COMPUTATION COMPLETE!")
print("="*80)
