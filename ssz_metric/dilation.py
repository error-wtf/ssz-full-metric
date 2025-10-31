"""
dilation.py
===========

Time dilation functions for SSZ and GR

© 2025 Carmen Wrede & Lino Casu
"""

import numpy as np
from .xi_field import xi_field

def D_SSZ(r, r_s):
    """
    SSZ time dilation factor
    
    Formula: D_SSZ = 1 / (1 + Ξ(r))
    
    Parameters:
    -----------
    r : float or array
        Radial coordinate [m]
    r_s : float
        Schwarzschild radius [m]
    
    Returns:
    --------
    D : float or array
        SSZ time dilation factor (dimensionless)
    """
    Xi = xi_field(r, r_s)
    return 1.0 / (1.0 + Xi)

def D_GR(r, r_s):
    """
    GR (Schwarzschild) time dilation factor
    
    Formula: D_GR = sqrt(1 - r_s/r)
    
    Parameters:
    -----------
    r : float or array
        Radial coordinate [m]
    r_s : float
        Schwarzschild radius [m]
    
    Returns:
    --------
    D : float or array
        GR time dilation factor (dimensionless)
    """
    return np.sqrt(1.0 - r_s / r)
