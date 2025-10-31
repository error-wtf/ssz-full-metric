"""
deltaM.py
=========

Delta(M) mass correction for SSZ metric

© 2025 Carmen Wrede & Lino Casu
"""

import numpy as np

def delta_M(r_s):
    """
    Compute Δ(M) correction factor
    
    Formula: Δ(M) = 98.01·exp(-2.7177×10⁴·r_s) + 1.96
    
    This empirical correction ensures smooth behavior near the horizon.
    
    Parameters:
    -----------
    r_s : float
        Schwarzschild radius [m]
    
    Returns:
    --------
    Delta : float
        Correction factor Δ(M) (dimensionless, typically ≈ 2)
    """
    return 98.01 * np.exp(-2.7177e4 * r_s) + 1.96

def corrected_r_s(r_s_bare):
    """
    Apply Δ(M) correction to Schwarzschild radius
    
    Formula: r_s_corrected = r_s·(1 + Δ(M)/100)
    
    Parameters:
    -----------
    r_s_bare : float
        Bare Schwarzschild radius [m]
    
    Returns:
    --------
    r_s_corrected : float
        Corrected Schwarzschild radius [m]
    """
    Delta = delta_M(r_s_bare)
    return r_s_bare * (1.0 + Delta / 100.0)
