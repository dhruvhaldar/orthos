import numpy as np
from orthos.plate import solve_buckling

def test_critical_buckling_load():
    """
    Verifies N_cr calculation for a specific orthotropic plate.
    Reference: Jones, Mechanics of Composite Materials, Eq 5.25
    """

    # Known benchmark parameters
    D11, D12, D22, D66 = 100, 20, 50, 30
    a, b = 1.0, 1.0

    N_cr = solve_buckling(D11, D12, D22, D66, a, b, m=1, n=1)

    # Expected analytical result
    expected = (np.pi**2 / b**2) * (D11*(b/a)**2 + 2*(D12 + 2*D66) + D22*(a/b)**2)
    assert abs(N_cr - expected) < 1e-5
