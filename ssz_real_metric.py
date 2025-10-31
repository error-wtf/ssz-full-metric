"""
ssz_real_metric.py
===================

Dieses Modul implementiert den *vollständigen* metrischen Tensor der
Segmented‑Spacetime‑Theorie (SSZ) in sphärischer Symmetrie.  Die Formeln
folgen der Dokumentation in „Mathematische Formeln – Segmented Spacetime (SSZ)"
aus dem Repository `Segmented‑Spacetime‑Mass‑Projection‑Unified‑Results`.

Im SSZ‑Modell wird der Schwarzschild‑Lösung eine Serie von Termen
hinzugefügt, um die Segmentstruktur und Energie‑Bedingungen zu berücksichtigen.
Die resultierenden metrischen Funktionen `A(r)` und `B(r)` lauten

    A(r) = 1 - 2U + 2U**2 - (24/5)*U**3 + …,
    B(r) = 1/A(r),

wobei U(r) = G*M/(c**2 * r) der dimensionslose Schwachfeldparameter ist und
`G` die Gravitationskonstante, `c` die Lichtgeschwindigkeit sowie `M` die
Masse des zentralen Objekts.

Diese Implementierung trunciert die Serie bei O(U**3), wie im Paper
angegeben.  Für Anwendungen in schwachen Feldern ist diese Näherung
ausreichend; nahe des Horizonts (r ≈ r_s) sollte eine höhere Genauigkeit
durch zusätzliche Terme oder eine numerische Lösung gewählt werden.

Beachte: Die Winkelkomponenten r^2 und r^2*sin^2(theta) bleiben unverändert
gegenüber der Schwarzschild‑Metrik.  Der Tensor ist diagonal und hat die Signatur
(-,+,+,+).

Copyright © 2025 Carmen Wrede & Lino Casu.  Lizenz: Anti‑Capitalist Software
License v1.4.
"""

from __future__ import annotations

import os
import sys
import math
from typing import Tuple, Callable

# UTF-8 setup for Windows compatibility
os.environ['PYTHONIOENCODING'] = 'utf-8:replace'
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except:
        pass

# Physikalische Konstanten (SI)
G = 6.67430e-11  # m^3 kg^-1 s^-2
c = 2.99792458e8  # m s^-1


def schwarzschild_radius(mass: float) -> float:
    """Berechne den Schwarzschild‑Radius r_s = 2GM/c^2 für eine gegebene Masse.

    :param mass: Masse in Kilogramm
    :return: Schwarzschild‑Radius r_s in Metern
    """
    return 2.0 * G * mass / (c ** 2)


def weak_field_parameter(mass: float, r: float) -> float:
    """Berechne den dimensionslosen Schwachfeldparameter U(r).

    U(r) = r_s / (2r) = (G*M)/(c^2 * r).

    :param mass: Masse in Kilogramm
    :param r: radialer Koordinatenwert (m)
    :return: U(r)
    """
    return (G * mass) / (c ** 2 * r)


def metric_functions(mass: float, r: float) -> Tuple[float, float]:
    """Berechne die metrischen Funktionen A(r) und B(r) für die gegebene Masse.

    Das SSZ‑Modell nutzt eine Serie

        A(r) = 1 - 2U + 2U**2 + ε3*U**3
        B(r) = 1/A(r)

    mit ε3 = -24/5.

    :param mass: Masse in Kilogramm
    :param r: radialer Koordinatenwert (m)
    :return: Tuple (A(r), B(r))
    """
    U = weak_field_parameter(mass, r)
    epsilon3 = -24.0 / 5.0
    A = 1.0 - 2.0 * U + 2.0 * (U ** 2) + epsilon3 * (U ** 3)
    # Zusätzliche Terme höherer Ordnung können hier hinzugefügt werden
    # wenn erforderlich, z.B. A += epsilon4 * U**4
    if A == 0:
        # Vermeiden einer Division durch Null; B wird unendlich
        B = float('inf')
    else:
        B = 1.0 / A
    return A, B


def metric_tensor(mass: float, r: float, theta: float) -> Tuple[Tuple[float, float, float, float], ...]:
    """Berechne den vollständigen diagonalen metrischen Tensor g_{μν}(r,θ) im SSZ‑Modell.

    Die Metrik hat die Form

        ds² = -A(r) dt² + B(r) dr² + r² dθ² + r² sin²θ dφ².

    :param mass: Masse in Kilogramm
    :param r: radialer Koordinatenwert (m)
    :param theta: Polwinkel θ (Radiant)
    :return: 4×4‑Matrix des metrischen Tensors als verschachteltes Tuple
    """
    A, B = metric_functions(mass, r)
    # Diagonale Komponenten
    g_tt = -A
    g_rr = B
    g_thth = r ** 2
    g_phph = (r ** 2) * (math.sin(theta) ** 2)
    # 4×4 Tensor in der Reihenfolge (t,r,θ,φ)
    return (
        (g_tt, 0.0, 0.0, 0.0),
        (0.0, g_rr, 0.0, 0.0),
        (0.0, 0.0, g_thth, 0.0),
        (0.0, 0.0, 0.0, g_phph),
    )


def proper_time_dilation(mass: float, r: float) -> float:
    """Berechne die Zeitdilatation D(r) = √(-g_tt) relativ zur fernen Zeit.

    Dies entspricht der Anzahl an Eigenzeit‑Sekunden pro Koordinaten‑Sekunde für einen
    stationären Beobachter in radialer Entfernung r.  Beachte, dass dies die SSZ‑
    Zeitdilatation gemäß g_tt widerspiegelt und nicht die vereinfachte 1/(1+Ξ)‐Formel.

    :param mass: Masse in Kilogramm
    :param r: radialer Koordinatenwert (m)
    :return: D(r)
    """
    A, _ = metric_functions(mass, r)
    # Der Lorentzfaktor ist sqrt(|A|), da g_tt = -A; für A>0 ist g_tt<0.
    # Eine negative A bewirkt, dass g_tt positiv wird (Metrikwechsel);
    # in diesem Fall liefert abs(A) trotzdem einen reellen Wert.
    return math.sqrt(abs(A))


def demo_table(mass: float, r_min: float, r_max: float, num: int = 6) -> None:
    """Beispielhafter Tabellen‑Ausdruck der metrischen Koeffizienten für mehrere r‑Werte.

    Diese Funktion gibt eine einfache Tabelle im CSV‑Format auf stdout aus.
    Die Spalten enthalten r/r_s, A(r), B(r) sowie die SSZ‑ und GR‑Zeitdilatationen.

    :param mass: Masse in Kilogramm
    :param r_min: untere Grenze (m)
    :param r_max: obere Grenze (m)
    :param num: Anzahl der Abtastpunkte
    """
    r_s = schwarzschild_radius(mass)
    print("="*80)
    print("SSZ METRIC DEMONSTRATION")
    print("="*80)
    print(f"\nMass: {mass:.3e} kg")
    print(f"Schwarzschild radius r_s: {r_s:.3e} m ({r_s/1000:.3f} km)")
    print(f"Range: {r_min/r_s:.2f} r_s to {r_max/r_s:.2f} r_s")
    print()
    print("Post-Newtonian Expansion:")
    print("  A(r) = 1 - 2U + 2U² + ε₃U³")
    print("  where U = GM/(c²r) and ε₃ = -24/5")
    print()
    print("-"*80)
    print(f"{'r/r_s':<10} {'A(r)':<15} {'B(r)':<15} {'D_SSZ(r)':<15} {'D_GR(r)':<15}")
    print("-"*80)
    
    for i in range(num):
        r = r_min + (r_max - r_min) * i / (num - 1)
        A, B = metric_functions(mass, r)
        # SSZ‑Zeitdilatation aus g_tt
        D_ssz = proper_time_dilation(mass, r)
        # GR‑Zeitdilatation
        D_gr = math.sqrt(max(0.0, 1.0 - r_s / r))
        print(f"{r/r_s:<10.4f} {A:<15.6e} {B:<15.6e} {D_ssz:<15.6e} {D_gr:<15.6e}")
    
    print("-"*80)
    print()
    print("Physical Interpretation:")
    print("  • A(r): Temporal metric component (-A = g_tt)")
    print("  • B(r): Radial metric component (= 1/A for SSZ)")
    print("  • D_SSZ: Time dilation in SSZ (√A)")
    print("  • D_GR: Time dilation in GR (√(1-r_s/r))")
    print()
    print("Key differences:")
    print("  • SSZ includes O(U³) corrections → deviation from GR")
    print("  • Near r_s: SSZ predicts different behavior")
    print("  • Far field: SSZ → GR (as expected)")
    print("="*80)


if __name__ == "__main__":
    # Beispiel: 1 Sonnenmasse im Bereich [1.2 r_s, 5 r_s]
    M_sun = 1.98847e30  # kg
    r_sun = schwarzschild_radius(M_sun)
    
    print("\n" + "="*80)
    print("EXAMPLE 1: Sun (1 M☉)")
    print("="*80)
    demo_table(M_sun, 1.2 * r_sun, 5.0 * r_sun, num=8)
    
    print("\n" + "="*80)
    print("EXAMPLE 2: Stellar Black Hole (10 M☉)")
    print("="*80)
    M_bh = 10 * M_sun
    r_bh = schwarzschild_radius(M_bh)
    demo_table(M_bh, 1.5 * r_bh, 3.0 * r_bh, num=6)
    
    print("\n" + "="*80)
    print("EXAMPLE 3: Near Natural Boundary (φ/2 × r_s)")
    print("="*80)
    phi = (1 + math.sqrt(5)) / 2  # Golden ratio
    r_phi = (phi / 2) * r_sun
    print(f"φ = {phi:.10f} (golden ratio)")
    print(f"r_φ = (φ/2) × r_s = {r_phi/r_sun:.4f} r_s")
    print()
    demo_table(M_sun, r_phi, 2.0 * r_sun, num=6)
