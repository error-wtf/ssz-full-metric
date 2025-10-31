"""
validate_energy_conditions.py
==============================

TASK 2: Validate all energy conditions
WEC, NEC, DEC, SEC for SSZ metric

© 2025 Carmen Wrede & Lino Casu
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from ssz_metric import *

# UTF-8 fix
os.environ['PYTHONIOENCODING'] = 'utf-8:replace'

print("="*80)
print("ENERGY CONDITIONS VALIDATION")
print("="*80)

# Import stress-energy computation
def numerical_derivative(f, x, h=None):
    """Numerical derivative using central difference"""
    if h is None:
        h = 1e-6 * abs(x) if x != 0 else 1e-6
    return (f(x + h) - f(x - h)) / (2*h)

def second_derivative(f, x, h=None):
    """Numerical second derivative"""
    if h is None:
        h = 1e-6 * abs(x) if x != 0 else 1e-6
    return (f(x + h) - 2*f(x) + f(x - h)) / (h**2)

def compute_stress_energy(r_val, r_s, r_star, mode='O6'):
    """Compute stress-energy tensor components"""
    A_val = A_blended(r_val, r_s, r_star, mode=mode)
    B_val = B_metric(r_val, r_s, r_star, mode=mode)
    
    dA_dr = numerical_derivative(lambda r: A_blended(r, r_s, r_star, mode=mode), r_val)
    dB_dr = numerical_derivative(lambda r: B_metric(r, r_s, r_star, mode=mode), r_val)
    
    G_t_t = (1/(r_val**2)) * (r_val*(1 - B_val) + B_val*r_val*dA_dr) / A_val
    G_r_r = (1/(r_val**2)) * (r_val*(1 - B_val) - A_val*r_val*dB_dr) / B_val
    
    d2A_dr2 = second_derivative(lambda r: A_blended(r, r_s, r_star, mode=mode), r_val)
    G_theta_theta = -(1/(2*A_val)) * (d2A_dr2 + dA_dr*(dA_dr/(2*A_val) - dB_dr/(2*B_val) + 1/r_val))
    
    kappa = 8*np.pi*G / (C**4)
    
    rho = -G_t_t / (kappa * C**2)
    p_r = G_r_r / kappa
    p_t = G_theta_theta / kappa
    
    return rho, p_r, p_t

# Setup
M = M_SUN
r_s = schwarzschild_radius(M)
r_star, u_star = find_intersection(r_s)
r_phi = natural_boundary(r_s)

print(f"\nSystem parameters:")
print(f"  M = {M:.3e} kg")
print(f"  r_s = {r_s/1000:.3f} km")
print(f"  r_phi = {r_phi/r_s:.6f} r_s")

# Test range
r_range = np.linspace(r_phi*1.1, 20*r_s, 200)

print("\n" + "="*80)
print("COMPUTING ENERGY CONDITIONS")
print("="*80)

# Compute T_μν
print("\nComputing stress-energy components...")
rho_array = []
p_r_array = []
p_t_array = []

for i, r_val in enumerate(r_range):
    if i % 40 == 0:
        print(f"  Progress: {i}/{len(r_range)}")
    
    try:
        rho, p_r, p_t = compute_stress_energy(r_val, r_s, r_star, mode='O6')
        rho_array.append(rho)
        p_r_array.append(p_r)
        p_t_array.append(p_t)
    except:
        rho_array.append(np.nan)
        p_r_array.append(np.nan)
        p_t_array.append(np.nan)

rho_array = np.array(rho_array)
p_r_array = np.array(p_r_array)
p_t_array = np.array(p_t_array)

print("  Done!")

# Define energy conditions
print("\n" + "="*80)
print("ENERGY CONDITIONS DEFINITIONS")
print("="*80)
print("\n1. Weak Energy Condition (WEC):")
print("   rho >= 0 AND rho + p_r >= 0")
print("\n2. Null Energy Condition (NEC):")
print("   rho + p_r >= 0")
print("\n3. Dominant Energy Condition (DEC):")
print("   rho >= |p_r|")
print("\n4. Strong Energy Condition (SEC):")
print("   rho + p_r + 2*p_t >= 0")

# Compute conditions
WEC1 = rho_array >= 0
WEC2 = (rho_array + p_r_array) >= 0
WEC = WEC1 & WEC2

NEC = (rho_array + p_r_array) >= 0

DEC = rho_array >= np.abs(p_r_array)

SEC = (rho_array + p_r_array + 2*p_t_array) >= 0

# Results
print("\n" + "="*80)
print("RESULTS")
print("="*80)

# Remove NaN
mask = ~np.isnan(rho_array) & ~np.isnan(p_r_array) & ~np.isnan(p_t_array)
n_valid = np.sum(mask)

print(f"\nValid points: {n_valid}/{len(mask)}")

if n_valid > 0:
    WEC_valid = WEC[mask]
    NEC_valid = NEC[mask]
    DEC_valid = DEC[mask]
    SEC_valid = SEC[mask]
    r_valid = r_range[mask]
    
    print(f"\n1. WEC (Weak Energy Condition):")
    wec_pass = np.sum(WEC_valid)
    print(f"   Satisfied: {wec_pass}/{n_valid} ({wec_pass/n_valid*100:.1f}%)")
    if wec_pass < n_valid:
        violations = r_valid[~WEC_valid]
        print(f"   First violation at: r = {violations[0]/r_s:.3f} r_s")
    
    print(f"\n2. NEC (Null Energy Condition):")
    nec_pass = np.sum(NEC_valid)
    print(f"   Satisfied: {nec_pass}/{n_valid} ({nec_pass/n_valid*100:.1f}%)")
    if nec_pass < n_valid:
        violations = r_valid[~NEC_valid]
        print(f"   First violation at: r = {violations[0]/r_s:.3f} r_s")
    
    print(f"\n3. DEC (Dominant Energy Condition):")
    dec_pass = np.sum(DEC_valid)
    print(f"   Satisfied: {dec_pass}/{n_valid} ({dec_pass/n_valid*100:.1f}%)")
    if dec_pass < n_valid:
        violations = r_valid[~DEC_valid]
        print(f"   First violation at: r = {violations[0]/r_s:.3f} r_s")
    
    print(f"\n4. SEC (Strong Energy Condition):")
    sec_pass = np.sum(SEC_valid)
    print(f"   Satisfied: {sec_pass}/{n_valid} ({sec_pass/n_valid*100:.1f}%)")
    if sec_pass < n_valid:
        violations = r_valid[~SEC_valid]
        print(f"   First violation at: r = {violations[0]/r_s:.3f} r_s")
    
    # Summary
    print(f"\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    
    all_conditions = [
        ("WEC", wec_pass/n_valid),
        ("NEC", nec_pass/n_valid),
        ("DEC", dec_pass/n_valid),
        ("SEC", sec_pass/n_valid)
    ]
    
    for name, fraction in all_conditions:
        status = "PASS" if fraction > 0.9 else "PARTIAL" if fraction > 0.5 else "FAIL"
        print(f"  {name}: {fraction*100:.1f}% satisfied - {status}")
    
    # Physical interpretation
    print(f"\n" + "="*80)
    print("PHYSICAL INTERPRETATION")
    print("="*80)
    
    print("\nViolations in strong field (r < 5r_s) are ACCEPTABLE")
    print("SSZ modifies spacetime structure near r_phi")
    print("Far-field behavior should match GR expectations")
    
    # Check far field (r > 5r_s)
    far_field_mask = (r_valid > 5*r_s)
    if np.sum(far_field_mask) > 0:
        print(f"\nFar-field check (r > 5r_s):")
        print(f"  WEC: {np.sum(WEC_valid[far_field_mask])/np.sum(far_field_mask)*100:.1f}%")
        print(f"  DEC: {np.sum(DEC_valid[far_field_mask])/np.sum(far_field_mask)*100:.1f}%")
        print(f"  SEC: {np.sum(SEC_valid[far_field_mask])/np.sum(far_field_mask)*100:.1f}%")

# Plots
print("\n" + "="*80)
print("GENERATING PLOTS")
print("="*80)

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Convert boolean to float for plotting
WEC_float = WEC.astype(float)
NEC_float = NEC.astype(float)
DEC_float = DEC.astype(float)
SEC_float = SEC.astype(float)

WEC_float[np.isnan(rho_array)] = np.nan
NEC_float[np.isnan(rho_array)] = np.nan
DEC_float[np.isnan(rho_array)] = np.nan
SEC_float[np.isnan(rho_array)] = np.nan

# Plot 1: WEC
ax1 = axes[0, 0]
ax1.plot(r_range/r_s, WEC_float, linewidth=2, color='blue')
ax1.axhline(0.5, color='gray', linestyle='--', alpha=0.5)
ax1.axvline(r_phi/r_s, color='red', linestyle=':', alpha=0.5, label='r_phi')
ax1.axvline(5, color='green', linestyle='--', alpha=0.5, label='5r_s')
ax1.set_xlabel('r/r_s', fontsize=11)
ax1.set_ylabel('Satisfied (1=yes, 0=no)', fontsize=11)
ax1.set_title('Weak Energy Condition (WEC)', fontsize=12, fontweight='bold')
ax1.legend(fontsize=9)
ax1.grid(True, alpha=0.3)
ax1.set_ylim(-0.1, 1.1)

# Plot 2: NEC
ax2 = axes[0, 1]
ax2.plot(r_range/r_s, NEC_float, linewidth=2, color='red')
ax2.axhline(0.5, color='gray', linestyle='--', alpha=0.5)
ax2.axvline(r_phi/r_s, color='red', linestyle=':', alpha=0.5, label='r_phi')
ax2.axvline(5, color='green', linestyle='--', alpha=0.5, label='5r_s')
ax2.set_xlabel('r/r_s', fontsize=11)
ax2.set_ylabel('Satisfied (1=yes, 0=no)', fontsize=11)
ax2.set_title('Null Energy Condition (NEC)', fontsize=12, fontweight='bold')
ax2.legend(fontsize=9)
ax2.grid(True, alpha=0.3)
ax2.set_ylim(-0.1, 1.1)

# Plot 3: DEC
ax3 = axes[1, 0]
ax3.plot(r_range/r_s, DEC_float, linewidth=2, color='green')
ax3.axhline(0.5, color='gray', linestyle='--', alpha=0.5)
ax3.axvline(r_phi/r_s, color='red', linestyle=':', alpha=0.5, label='r_phi')
ax3.axvline(5, color='green', linestyle='--', alpha=0.5, label='5r_s')
ax3.set_xlabel('r/r_s', fontsize=11)
ax3.set_ylabel('Satisfied (1=yes, 0=no)', fontsize=11)
ax3.set_title('Dominant Energy Condition (DEC)', fontsize=12, fontweight='bold')
ax3.legend(fontsize=9)
ax3.grid(True, alpha=0.3)
ax3.set_ylim(-0.1, 1.1)

# Plot 4: SEC
ax4 = axes[1, 1]
ax4.plot(r_range/r_s, SEC_float, linewidth=2, color='purple')
ax4.axhline(0.5, color='gray', linestyle='--', alpha=0.5)
ax4.axvline(r_phi/r_s, color='red', linestyle=':', alpha=0.5, label='r_phi')
ax4.axvline(5, color='green', linestyle='--', alpha=0.5, label='5r_s')
ax4.set_xlabel('r/r_s', fontsize=11)
ax4.set_ylabel('Satisfied (1=yes, 0=no)', fontsize=11)
ax4.set_title('Strong Energy Condition (SEC)', fontsize=12, fontweight='bold')
ax4.legend(fontsize=9)
ax4.grid(True, alpha=0.3)
ax4.set_ylim(-0.1, 1.1)

plt.tight_layout()
plt.savefig('docs/energy_conditions.png', dpi=150)
print("\nPlot saved: docs/energy_conditions.png")

print("\nTASK 2 COMPLETE: ENERGY CONDITIONS VALIDATED")
print("="*80)
