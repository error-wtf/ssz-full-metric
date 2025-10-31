"""
constants.py
============

Fundamental constants for SSZ metric

© 2025 Carmen Wrede & Lino Casu
"""

import math

# Golden ratio
PHI = (1 + math.sqrt(5)) / 2

# Physical constants (SI units)
C = 2.99792458e8      # Speed of light [m/s]
G = 6.67430e-11       # Gravitational constant [m³/(kg·s²)]
M_SUN = 1.98847e30    # Solar mass [kg]

# Derived constants
def schwarzschild_radius(M):
    """Compute Schwarzschild radius for mass M"""
    return 2 * G * M / (C**2)

# Solar values (for reference)
R_S_SUN = schwarzschild_radius(M_SUN)  # ≈ 2953 m
