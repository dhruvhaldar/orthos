import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def get_Q_matrix(E1, E2, G12, nu12):
    nu21 = nu12 * E2 / E1
    denom = 1 - nu12 * nu21
    Q11 = E1 / denom
    Q22 = E2 / denom
    Q12 = nu12 * E2 / denom
    Q66 = G12
    return np.array([[Q11, Q12, 0], [Q12, Q22, 0], [0, 0, Q66]])

def rotate_Q(Q, angle_deg):
    theta = np.radians(angle_deg)
    c = np.cos(theta)
    s = np.sin(theta)

    Q11, Q12, Q22 = Q[0,0], Q[0,1], Q[1,1]
    Q66 = Q[2,2]

    c2 = c*c
    s2 = s*s
    c4 = c2*c2
    s4 = s2*s2

    Qbar11 = Q11*c4 + 2*(Q12 + 2*Q66)*s2*c2 + Q22*s4
    Qbar12 = (Q11 + Q22 - 4*Q66)*s2*c2 + Q12*(c4 + s4)
    Qbar22 = Q11*s4 + 2*(Q12 + 2*Q66)*s2*c2 + Q22*c4
    Qbar16 = (Q11 - Q12 - 2*Q66)*s*c**3 + (Q12 - Q22 + 2*Q66)*s**3*c
    Qbar26 = (Q11 - Q12 - 2*Q66)*s**3*c + (Q12 - Q22 + 2*Q66)*s*c**3
    Qbar66 = (Q11 + Q22 - 2*Q12 - 2*Q66)*s2*c2 + Q66*(c4 + s4)

    return np.array([
        [Qbar11, Qbar12, Qbar16],
        [Qbar12, Qbar22, Qbar26],
        [Qbar16, Qbar26, Qbar66]
    ])

class RectangularPlate:
    def __init__(self, length, width, layup, sym=False, E1=140e9, E2=10e9, G12=5e9, nu12=0.3, ply_thickness=0.000125):
        self.a = length
        self.b = width
        self.layup = layup
        self.sym = sym

        if sym:
            full_layup = layup + layup[::-1]
        else:
            full_layup = layup

        n_plies = len(full_layup)
        h = n_plies * ply_thickness
        self.h = h
        self.full_layup = full_layup

        # Z coordinates
        z = np.linspace(-h/2, h/2, n_plies + 1)

        Q = get_Q_matrix(E1, E2, G12, nu12)

        self.D = np.zeros((3, 3))

        for i in range(n_plies):
            angle = full_layup[i]
            Qbar = rotate_Q(Q, angle)
            # D_ij = sum(Qbar_ij * (z_k^3 - z_{k-1}^3) / 3)
            self.D += Qbar * (z[i+1]**3 - z[i]**3) / 3.0

    def solve_bending(self, load, method='navier', m_max=11, n_max=11):
        """
        Navier solution for SS-SS-SS-SS plate under uniform load q0.
        Returns deflection matrix w.
        """
        if method != 'navier':
            raise NotImplementedError("Only Navier solution is implemented.")

        D11 = self.D[0,0]
        D12 = self.D[0,1]
        D22 = self.D[1,1]
        D66 = self.D[2,2]

        # Check for D16 and D26. If they are significant, Navier solution for "Specially Orthotropic"
        # is an approximation or incorrect. For this educational tool, we proceed with D11, D12, D22, D66.
        # Ideally, we should warn if D16/D26 are non-zero.

        X = np.linspace(0, self.a, 50)
        Y = np.linspace(0, self.b, 50)
        X, Y = np.meshgrid(X, Y)
        w = np.zeros_like(X)

        # Navier series for Uniform Load
        for m in range(1, m_max, 2): # Odd terms only
            for n in range(1, n_max, 2):
                alpha = m * np.pi / self.a
                beta = n * np.pi / self.b

                # Load coefficient Pmn for uniform load q0
                Pmn = (16 * load) / (np.pi**2 * m * n)

                D_term = D11*alpha**4 + 2*(D12 + 2*D66)*alpha**2*beta**2 + D22*beta**4

                Wmn = Pmn / D_term

                w += Wmn * np.sin(alpha * X) * np.sin(beta * Y)

        return w

    def plot_surface(self, w):
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')

        x = np.linspace(0, self.a, w.shape[1])
        y = np.linspace(0, self.b, w.shape[0])
        X, Y = np.meshgrid(x, y)

        surf = ax.plot_surface(X, Y, w, cmap='viridis')
        fig.colorbar(surf)
        ax.set_xlabel('Length (x)')
        ax.set_ylabel('Width (y)')
        ax.set_zlabel('Deflection (w)')
        plt.title('Plate Deflection')

        if plt.get_backend() != 'agg':
             plt.show()

def solve_buckling(D11, D12, D22, D66, a, b, m=1, n=1):
    """
    Calculates Critical Buckling Load N_cr for a specially orthotropic plate.
    N_x_cr = (pi^2 / b^2) * [D11*(m*b/a)^2 + 2*(D12 + 2*D66) + D22*(a/m*b)^2 * n^2/m^2??]

    Actually, let's look at Jones Eq 5.25 form (uniaxial compression N_x).
    For m half-waves in x and n half-waves in y:
    N_x = pi^2 * [D11(m/a)^4 + 2(D12+2D66)(m/a)^2(n/b)^2 + D22(n/b)^4] / (m/a)^2
        = pi^2 * [D11(m/a)^2 + 2(D12+2D66)(n/b)^2 + D22(n/b)^4 / (m/a)^2]

    Rearranging to match the test expectation:
    expected = (np.pi**2 / b**2) * (D11*(b/a)**2 + 2*(D12 + 2*D66) + D22*(a/b)**2)
    This corresponds to m=1, n=1.

    Let's implement the general form for N_x.
    N_x = (pi^2 / b^2) * (D11*(m*b/(n*a))**2 + 2*(D12 + 2*D66) + D22*(n*a/(m*b))**2) * n^2?

    Wait.
    Numerator: D11(m/a)^4 + ...
    Denominator: (m/a)^2
    Result: D11(m/a)^2 + 2(D12+2D66)(n/b)^2 + D22(n/b)^4 * (a/m)^2
          = D11(m/a)^2 + 2(D12+2D66)(n/b)^2 + D22 * (n^4 a^2 / b^4 m^2)

    If m=1, n=1:
    = D11(1/a)^2 + 2(D12+2D66)(1/b)^2 + D22(1/b)^4 * a^2
    = D11/a^2 + 2(D12+2D66)/b^2 + D22 * a^2/b^4
    Factor out (pi^2 / b^2):
    = (pi^2/b^2) * [ D11 * b^2/a^2 + 2(D12+2D66) + D22 * a^2/b^2 ]

    This matches the expected formula.

    So the generalized formula I should use is:
    N_cr = (np.pi**2 / b**2) * (D11*(m*b/a)**2 + 2*(D12 + 2*D66)*n**2 + D22*(n**4 * a**2 / (m**2 * b**2)))

    Wait, let's check the algebra again.
    Term 3: D22(n/b)^4 / (m/a)^2 = D22 * (n^4/b^4) * (a^2/m^2) = D22 * (a/b)^2 * (n^4/m^2) / b^2
    Inside the bracket (factored out 1/b^2):
    D22 * (a/b)^2 * (n^4/m^2)

    If n=1, m=1: D22 * (a/b)^2. Correct.

    So the function:
    """
    term1 = D11 * (m * b / a)**2
    term2 = 2 * (D12 + 2 * D66) * n**2
    term3 = D22 * (a * n**2 / (b * m))**2 # Check: D22 * a^2 n^4 / (b^2 m^2) = D22 * (a/b)^2 * (n^4/m^2). Correct.

    return (np.pi**2 / b**2) * (term1 + term2 + term3)
