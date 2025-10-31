"""
match_blend.py
==============

Find intersection point r_star where D_SSZ = D_GR

© 2025 Carmen Wrede & Lino Casu
"""

import numpy as np
from scipy.optimize import brentq
from .constants import PHI
from .dilation import D_SSZ, D_GR

def intersection_equation(u, phi=PHI):
    """
    Equation whose root gives the intersection point u*
    
    Formula: 1/(2 - exp(-φ·u)) = sqrt(1 - 1/u)
    
    Parameters:
    -----------
    u : float
        Dimensionless radius u = r/r_s
    phi : float, optional
        Golden ratio (default: PHI)
    
    Returns:
    --------
    residual : float
        Difference between D_SSZ and D_GR
    """
    D_ssz = 1.0 / (2.0 - np.exp(-phi * u))
    D_gr = np.sqrt(1.0 - 1.0 / u)
    return D_ssz - D_gr

def find_intersection(r_s, u_min=1.1, u_max=3.0):
    """
    Find intersection radius r_star where D_SSZ = D_GR
    
    Uses Brent's root finding method for robustness.
    
    Parameters:
    -----------
    r_s : float
        Schwarzschild radius [m]
    u_min : float, optional
        Minimum search u value (default: 1.1)
    u_max : float, optional
        Maximum search u value (default: 3.0)
    
    Returns:
    --------
    r_star : float
        Intersection radius [m]
    u_star : float
        Dimensionless intersection point u* = r_star/r_s
    """
    # Find u* using Brent's method
    try:
        u_star = brentq(intersection_equation, u_min, u_max, xtol=1e-12)
    except ValueError as e:
        # Fallback to known canonical value
        print(f"Warning: Root finding failed, using canonical value")
        u_star = 1.386562
    
    r_star = u_star * r_s
    
    return r_star, u_star

def verify_intersection(r_star, r_s, tol=1e-6):
    """
    Verify that r_star is indeed the intersection point
    
    Parameters:
    -----------
    r_star : float
        Intersection radius [m]
    r_s : float
        Schwarzschild radius [m]
    tol : float, optional
        Tolerance for verification (default: 1e-6)
    
    Returns:
    --------
    verified : bool
        True if |D_SSZ - D_GR| < tol at r_star
    difference : float
        Actual difference |D_SSZ - D_GR|
    """
    D_ssz = D_SSZ(r_star, r_s)
    D_gr = D_GR(r_star, r_s)
    
    diff = abs(D_ssz - D_gr)
    verified = diff < tol
    
    return verified, diff
