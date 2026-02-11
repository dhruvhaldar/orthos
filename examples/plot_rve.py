from orthos.micromechanics import HalpinTsai

# Carbon Fiber / Epoxy Matrix
results = HalpinTsai.scan_volume_fraction(
    E_f=230e9, E_m=3.0e9,   # Fiber/Matrix Modulus
    xi=2.0,                 # Reinforcement factor
    vf_range=[0.0, 0.7]     # 0% to 70% Fiber Volume
)

print("Plotting Micromechanics Results...")
results.plot()
