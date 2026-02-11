import numpy as np

def predict_strength_psc(unnotched_strength, R, d0):
    """
    Predicts notched strength using Point Stress Criterion (Whitney-Nuismer).

    Assumption: Uses isotropic stress concentration decay for the stress field approximation
    as material properties are not provided in this function signature.

    sigma_y(x, 0) ~= sigma_inf * [1 + 0.5(R/x)^2 + 1.5(R/x)^4]

    Failure condition: sigma_y(R+d0) = unnotched_strength
    => sigma_N * Kt_d0 = unnotched_strength
    => sigma_N = unnotched_strength / Kt_d0
    """
    x = R + d0
    xi = R / x
    Kt_d0 = 1 + 0.5 * xi**2 + 1.5 * xi**4

    return unnotched_strength / Kt_d0

class AnisotropicHole:
    def __init__(self, Ex, Ey, Gxy, nuxy, R):
        self.Ex = Ex
        self.Ey = Ey
        self.Gxy = Gxy
        self.nuxy = nuxy
        self.R = R

    def get_boundary_stress(self, theta_deg, sigma_inf=1.0):
        """
        Calculates hoop stress at the hole boundary (r=R) for an infinite orthotropic plate
        under uniaxial tension sigma_inf along x-axis.

        Formula from Lekhnitskii:
        sigma_theta = sigma_inf * (Ey/Ex) *
          [ -cos^2 theta + (k+n)*sin^2 theta ] /
          [ sin^4 theta + (n^2 - 2k)*sin^2 theta cos^2 theta + k^2 cos^4 theta ]

        where k = sqrt(Ey/Ex)
              n = sqrt(2*(sqrt(Ey/Ex) - nu_yx) + Ey/Gxy)
        """
        theta_rad = np.radians(theta_deg)
        c = np.cos(theta_rad)
        s = np.sin(theta_rad)

        k = np.sqrt(self.Ey / self.Ex)
        nu_yx = self.nuxy * self.Ey / self.Ex
        n = np.sqrt(2 * (k - nu_yx) + self.Ey / self.Gxy)

        num = -c**2 + (k + n) * s**2
        den = s**4 + (n**2 - 2*k) * s**2 * c**2 + k**2 * c**4

        return sigma_inf * (self.Ey / self.Ex) * num / den
