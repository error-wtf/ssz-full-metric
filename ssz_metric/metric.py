"""
metric.py
=========

Full SSZ metric with smooth blending

© 2025 Carmen Wrede & Lino Casu
"""

import numpy as np
from .constants import PHI
from .xi_field import xi_field
from .deltaM import delta_M

# Post-Newtonian coefficient
EPS_3 = -24.0 / 5.0  # = -4.8

def A_PNDelta(r, r_s):
    """
    Post-Newtonian metric coefficient with Δ(M) correction
    
    Formula: A_PNΔ(r) = 1 - 2U + 2U² + ε₃U³
    where U = r_s/(2r) and r_s → r_s(1 + Δ(M)/100)
    
    Parameters:
    -----------
    r : float or array
        Radial coordinate [m]
    r_s : float
        Bare Schwarzschild radius [m]
    
    Returns:
    --------
    A : float or array
        PN metric coefficient (dimensionless)
    """
    # Apply Δ(M) correction
    Delta = delta_M(r_s)
    r_s_corr = r_s * (1.0 + Delta / 100.0)
    
    # Weak field parameter
    U = r_s_corr / (2.0 * r)
    
    # Post-Newtonian expansion
    A = 1.0 - 2.0*U + 2.0*U**2 + EPS_3*U**3
    
    return A

def A_Xi(r, r_s):
    """
    SSZ metric coefficient from segment density
    
    Formula: A_Ξ(r) = (1 + Ξ(r))^(-2) = D_SSZ²
    
    Parameters:
    -----------
    r : float or array
        Radial coordinate [m]
    r_s : float
        Schwarzschild radius [m]
    
    Returns:
    --------
    A : float or array
        SSZ metric coefficient (dimensionless)
    """
    Xi = xi_field(r, r_s)
    return (1.0 + Xi)**(-2)

def w_blend(r, r_star, ell):
    """
    Smooth blending function
    
    Formula: w(r) = ½(1 + tanh((r_star - r)/ℓ))
    
    Parameters:
    -----------
    r : float or array
        Radial coordinate [m]
    r_star : float
        Intersection radius [m]
    ell : float
        Smoothing scale [m]
    
    Returns:
    --------
    w : float or array
        Blending weight (0 to 1)
    """
    return 0.5 * (1.0 + np.tanh((r_star - r) / ell))

def A_blended(r, r_s, r_star, ell=None):
    """
    Full SSZ metric coefficient with smooth blending
    
    Formula: A(r) = w(r)·A_Ξ(r) + (1-w(r))·A_PNΔ(r)
    
    Parameters:
    -----------
    r : float or array
        Radial coordinate [m]
    r_s : float
        Schwarzschild radius [m]
    r_star : float
        Intersection radius [m]
    ell : float, optional
        Smoothing scale [m]. Default: 0.05·r_s
    
    Returns:
    --------
    A : float or array
        Blended metric coefficient (dimensionless)
    """
    if ell is None:
        ell = 0.05 * r_s
    
    # Compute both metric forms
    A_pn = A_PNDelta(r, r_s)
    A_xi = A_Xi(r, r_s)
    
    # Blending weight
    w = w_blend(r, r_star, ell)
    
    # Smooth blend
    A = w * A_xi + (1.0 - w) * A_pn
    
    return A

def B_metric(r, r_s, r_star, ell=None):
    """
    Radial metric coefficient
    
    Formula: B(r) = 1/A(r) (isotropic assumption)
    
    Later: can be computed consistently from Einstein equations
    
    Parameters:
    -----------
    r : float or array
        Radial coordinate [m]
    r_s : float
        Schwarzschild radius [m]
    r_star : float
        Intersection radius [m]
    ell : float, optional
        Smoothing scale [m]
    
    Returns:
    --------
    B : float or array
        Radial metric coefficient (dimensionless)
    """
    A = A_blended(r, r_s, r_star, ell)
    return 1.0 / A

def natural_boundary(r_s):
    """
    Compute natural boundary radius r_φ
    
    Formula: r_φ = (φ/2)·r_s·(1 + Δ(M)/100)
    
    Parameters:
    -----------
    r_s : float
        Schwarzschild radius [m]
    
    Returns:
    --------
    r_phi : float
        Natural boundary radius [m]
    """
    Delta = delta_M(r_s)
    return (PHI / 2.0) * r_s * (1.0 + Delta / 100.0)
