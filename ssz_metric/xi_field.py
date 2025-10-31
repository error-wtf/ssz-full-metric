"""
xi_field.py
===========

Segment density field Ξ(r) for SSZ theory

© 2025 Carmen Wrede & Lino Casu
"""

import numpy as np
from .constants import PHI

def xi_field(r, r_s):
    """
    Compute segment density Ξ(r)
    
    Formula: Ξ(r) = 1 - exp(-φ·r/r_s)
    
    Parameters:
    -----------
    r : float or array
        Radial coordinate [m]
    r_s : float
        Schwarzschild radius [m]
    
    Returns:
    --------
    Xi : float or array
        Segment density (dimensionless)
    """
    return 1.0 - np.exp(-PHI * r / r_s)
