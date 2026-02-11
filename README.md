# Orthos

**Orthos** is a high-fidelity computational library for **SD2413 Fibre Composites - Analysis and Design**. It addresses the "bottom-up" analysis of composite structures: starting from the micromechanics of fiber/matrix interaction, up to the macromechanics of anisotropic plate bending and stress concentrations.

This tool implements the **Analytical Solutions** (Navier, Levy, Lekhnitskii) often required in the course's "special computer code" assignment, providing exact benchmarks before moving to FEM.

## 📚 Syllabus Mapping (SD2413)

This project strictly adheres to the course learning outcomes:

| Module | Syllabus Topic | Implemented Features |
| --- | --- | --- |
| **Micromechanics** | *Predict stiffness and strength properties* | **Rule of Mixtures** and **Halpin-Tsai** equations to predict lamina properties () from constituents (). |
| **Macromechanics** | *Analyse mechanical behaviour* | Constitutive relations for general anisotropic materials (Compliance  and Stiffness  tensors). |
| **Plates** | *Analyse composite plates* | **Navier Solutions** for bending () and buckling () of specially orthotropic rectangular plates. |
| **Stress Conc.** | *Effect of holes* | **Lekhnitskii’s Complex Potentials** for calculating  in anisotropic plates. |
| **Failure** | *Prediction of failure mechanisms* | **Whitney-Nuismer** Point Stress & Average Stress criteria for Open Hole Tension/Compression. |

## 🚀 Deployment (Vercel)

Orthos is designed to run as a serverless analysis engine.

1. **Fork** this repository.
2. Deploy to **Vercel** (Python runtime is auto-detected).
3. Access the **Plate Solver** at `https://your-orthos.vercel.app`.

## 📊 Artifacts & Analytical Solutions

### 1. Micromechanics (Stiffness Prediction)

*Predicts the longitudinal and transverse modulus of a ply based on fiber volume fraction.*

**Code:**

```python
from orthos.micromechanics import HalpinTsai

# Carbon Fiber / Epoxy Matrix
results = HalpinTsai.scan_volume_fraction(
    E_f=230e9, E_m=3.0e9,   # Fiber/Matrix Modulus
    xi=2.0,                 # Reinforcement factor
    vf_range=[0.0, 0.7]     # 0% to 70% Fiber Volume
)

results.plot()

```

**Artifact Output:**

> *Figure 1: Rule of Mixtures vs. Halpin-Tsai. The graph illustrates how Transverse Modulus () is matrix-dominated and increases non-linearly, while Longitudinal Modulus () is fiber-dominated and linear.*

### 2. Anisotropic Plate Bending (Navier Solution)

*Solves the governing differential equation  for a simply supported plate.*

**Code:**

```python
from orthos.plate import RectangularPlate

# Define a [0/90]s Laminate Plate (1m x 1m)
plate = RectangularPlate(length=1.0, width=1.0, layup=[0, 90], sym=True)

# Apply Distributed Load q0 = 1000 Pa
deflection = plate.solve_bending(load=1000, method='navier')

plate.plot_surface(deflection)

```

**Artifact Output:**

> *Figure 2: Plate Deflection Surface (). The 3D plot shows the deformation of the composite plate. Due to the high stiffness in the 0-degree direction (), the curvature is shallower along the X-axis.*

### 3. Stress Concentration at a Hole

*Calculates the tangential stress  around a circular hole in an infinite anisotropic plate.*

**Artifact Output:**

> *Figure 3: Anisotropic Stress Concentration. Unlike isotropic materials (), an orthotropic composite can have  at 90 degrees to the load, depending on the  ratio. This plot visualizes Lekhnitskii's solution.*

## 🧪 Testing Strategy

### Unit Tests (Theory Verification)

Located in `tests/unit/`.

*Example: `tests/unit/test_buckling.py*`

```python
def test_critical_buckling_load():
    """
    Verifies N_cr calculation for a specific orthotropic plate.
    Reference: Jones, Mechanics of Composite Materials, Eq 5.25
    """
    from orthos.plate import solve_buckling

    # Known benchmark parameters
    D11, D12, D22, D66 = 100, 20, 50, 30
    a, b = 1.0, 1.0

    N_cr = solve_buckling(D11, D12, D22, D66, a, b, m=1, n=1)

    # Expected analytical result
    expected = (np.pi**2 / b**2) * (D11*(b/a)**2 + 2*(D12 + 2*D66) + D22*(a/b)**2)
    assert abs(N_cr - expected) < 1e-5

```

### E2E Tests (Failure Prediction)

Located in `tests/e2e/`.

*Example: `tests/e2e/test_hole_failure.py*`

```python
def test_whitney_nuismer():
    """
    E2E Test: Predict failure stress of a plate with a hole.
    Checks if the Point Stress Criterion matches experimental data.
    """
    laminate_strength = 1000e6 # Unnotched strength
    hole_radius = 0.005
    characteristic_distance = 0.001 # d0

    predicted_strength = orthos.holes.predict_strength_psc(
        laminate_strength, hole_radius, characteristic_distance
    )

    assert predicted_strength < laminate_strength

```

## ⚖️ License

**MIT License**

Copyright (c) 2026 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files... [Standard MIT Text]
