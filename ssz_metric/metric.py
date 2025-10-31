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

# Post-Newtonian coefficient (traditional)
EPS_3 = -24.0 / 5.0  # = -4.8

# φ-Series coefficients (discovered 2025-10-31)
# Pattern: c_{n+2} = (c_{n+1} + c_n) / φ
# These generate ε_n = c_n × φⁿ
PHI_SERIES_C = [
    1.0,        # c_0
    -2.0,       # c_1
    2.0,        # c_2
    -1.133126,  # c_3 (from ε_3 = -24/5)
    0.535758,   # c_4 (predicted via recursion)
    -0.369194,  # c_5 (predicted via recursion)
    0.102942,   # c_6 (predicted via recursion)
]

def A_phi_series(r, r_s, max_order=6, use_delta=True):
    """
    φ-Series metric coefficient with higher orders
    
    Formula: A(r) = Σ_{n=0}^{max_order} ε_n U^n
    where ε_n = c_n × φⁿ and U = r_s/(2r)
    
    This uses the discovered φ-series recursion:
    c_{n+2} = (c_{n+1} + c_n) / φ
    
    Parameters:
    -----------
    r : float or array
        Radial coordinate [m]
    r_s : float
        Bare Schwarzschild radius [m]
    max_order : int, optional
        Maximum order in expansion (default: 6)
    use_delta : bool, optional
        Apply Δ(M) correction (default: True)
    
    Returns:
    --------
    A : float or array
        φ-series metric coefficient (dimensionless)
    """
    # Apply Δ(M) correction if requested
    if use_delta:
        Delta = delta_M(r_s)
        r_s_eff = r_s * (1.0 + Delta / 100.0)
    else:
        r_s_eff = r_s
    
    # Weak field parameter
    U = r_s_eff / (2.0 * r)
    
    # φ-series expansion
    A = 0.0
    for n in range(min(max_order + 1, len(PHI_SERIES_C))):
        eps_n = PHI_SERIES_C[n] * (PHI ** n)
        A += eps_n * (U ** n)
    
    return A

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

def A_blended(r, r_s, r_star, ell=None, mode='O3'):
    """
    Full SSZ metric coefficient with smooth blending
    
    Formula: A(r) = w(r)·A_Ξ(r) + (1-w(r))·A_outer(r)
    
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
    mode : str, optional
        Outer metric mode:
        - 'O3': Traditional O(U³) with ε₃ = -24/5 (default)
        - 'O4': φ-series up to O(U⁴)
        - 'O5': φ-series up to O(U⁵)
        - 'O6': φ-series up to O(U⁶) (recommended)
    
    Returns:
    --------
    A : float or array
        Blended metric coefficient (dimensionless)
    """
    if ell is None:
        ell = 0.05 * r_s
    
    # Compute inner metric (always SSZ)
    A_xi = A_Xi(r, r_s)
    
    # Compute outer metric (mode-dependent)
    if mode == 'O3':
        A_pn = A_PNDelta(r, r_s)
    elif mode == 'O4':
        A_pn = A_phi_series(r, r_s, max_order=4)
    elif mode == 'O5':
        A_pn = A_phi_series(r, r_s, max_order=5)
    elif mode == 'O6':
        A_pn = A_phi_series(r, r_s, max_order=6)
    else:
        raise ValueError(f"Unknown mode: {mode}. Use 'O3', 'O4', 'O5', or 'O6'.")
    
    # Blending weight
    w = w_blend(r, r_star, ell)
    
    # Smooth blend
    A = w * A_xi + (1.0 - w) * A_pn
    
    return A

def B_metric(r, r_s, r_star, ell=None, mode='O3'):
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
    mode : str, optional
        Metric mode (see A_blended)
    
    Returns:
    --------
    B : float or array
        Radial metric coefficient (dimensionless)
    """
    A = A_blended(r, r_s, r_star, ell, mode=mode)
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
