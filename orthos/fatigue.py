import numpy as np
import matplotlib.pyplot as plt

class SNCurve:
    def __init__(self, A, B):
        """
        S-N Curve: sigma_max = A - B * log10(N)
        """
        self.A = A
        self.B = B

    def predict_life(self, stress_amplitude):
        """
        Predict cycles to failure N for a given stress amplitude.
        """
        if stress_amplitude >= self.A:
            return 0 # Immediate failure

        # A - B log10(N) = sigma
        # log10(N) = (A - sigma) / B
        # N = 10**((A - sigma) / B)
        return 10**((self.A - stress_amplitude) / self.B)

    def predict_strength(self, cycles):
        """
        Predict remaining strength or fatigue strength at N cycles.
        """
        if cycles <= 0:
            return self.A
        return self.A - self.B * np.log10(cycles)

    def plot(self, n_range=[1e3, 1e7]):
        N = np.logspace(np.log10(n_range[0]), np.log10(n_range[1]), 100)
        S = self.predict_strength(N)

        plt.figure(figsize=(10, 6))
        plt.semilogx(N, S / 1e6) # Plot in MPa usually
        plt.xlabel('Cycles to Failure (N)')
        plt.ylabel('Stress Amplitude (MPa)')
        plt.title('S-N Curve')
        plt.grid(True, which="both", ls="-")
        if plt.get_backend() != 'agg':
             plt.show()
