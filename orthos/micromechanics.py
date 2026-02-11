import numpy as np
import matplotlib.pyplot as plt

class MicromechanicsResult:
    def __init__(self, vf_range, E1, E2):
        self.vf_range = vf_range
        self.E1 = E1
        self.E2 = E2

    def plot(self):
        plt.figure(figsize=(10, 6))
        plt.plot(self.vf_range, self.E1 / 1e9, label='E1 (Longitudinal) - RoM')
        plt.plot(self.vf_range, self.E2 / 1e9, label='E2 (Transverse) - Halpin-Tsai')
        plt.xlabel('Fiber Volume Fraction')
        plt.ylabel('Modulus (GPa)')
        plt.title('Micromechanics: Rule of Mixtures vs Halpin-Tsai')
        plt.legend()
        plt.grid(True)
        # Check if running in a non-interactive environment (like tests)
        if plt.get_backend() != 'agg':
             plt.show()

class RuleOfMixtures:
    @staticmethod
    def calculate_E1(E_f, E_m, vf):
        """
        Calculate Longitudinal Modulus E1 using Rule of Mixtures.
        E1 = E_f * vf + E_m * (1 - vf)
        """
        return E_f * vf + E_m * (1 - vf)

    @staticmethod
    def calculate_E2_inverse(E_f, E_m, vf):
        """
        Calculate Transverse Modulus E2 using Inverse Rule of Mixtures.
        1/E2 = vf/E_f + (1-vf)/E_m
        """
        # Avoid division by zero if E_f or E_m is 0 (unlikely for physical materials)
        return 1.0 / (vf / E_f + (1 - vf) / E_m)

class HalpinTsai:
    @staticmethod
    def calculate_E2(E_f, E_m, vf, xi=2.0):
        """
        Calculate Transverse Modulus E2 using Halpin-Tsai equation.
        E2 = E_m * (1 + xi * eta * vf) / (1 - eta * vf)
        where eta = (E_f/E_m - 1) / (E_f/E_m + xi)
        """
        eta = (E_f / E_m - 1) / (E_f / E_m + xi)
        return E_m * (1 + xi * eta * vf) / (1 - eta * vf)

    @classmethod
    def scan_volume_fraction(cls, E_f, E_m, xi=2.0, vf_range=[0.0, 0.7]):
        """
        Generates E1 (Rule of Mixtures) and E2 (Halpin-Tsai) for a range of volume fractions.
        """
        vfs = np.linspace(vf_range[0], vf_range[1], 100)

        # E1 is typically calculated using Rule of Mixtures
        E1 = RuleOfMixtures.calculate_E1(E_f, E_m, vfs)

        # E2 using Halpin-Tsai
        E2 = cls.calculate_E2(E_f, E_m, vfs, xi)

        return MicromechanicsResult(vfs, E1, E2)
