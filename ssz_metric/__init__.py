"""
SSZ Full Metric Package
=======================

Singularity-free Segmented Spacetime metric

© 2025 Carmen Wrede & Lino Casu
"""

from .constants import PHI, C, G, M_SUN, schwarzschild_radius
from .xi_field import xi_field
from .dilation import D_SSZ, D_GR
from .deltaM import delta_M, corrected_r_s
from .metric import (
    A_PNDelta, A_Xi, A_blended, B_metric,
    natural_boundary, w_blend
)
from .match_blend import (
    find_intersection, verify_intersection,
    intersection_equation
)

__version__ = "1.0.0"
__all__ = [
    # Constants
    'PHI', 'C', 'G', 'M_SUN', 'schwarzschild_radius',
    # Segment density
    'xi_field',
    # Time dilation
    'D_SSZ', 'D_GR',
    # Mass correction
    'delta_M', 'corrected_r_s',
    # Metric coefficients
    'A_PNDelta', 'A_Xi', 'A_blended', 'B_metric',
    'natural_boundary', 'w_blend',
    # Matching
    'find_intersection', 'verify_intersection',
    'intersection_equation',
]
