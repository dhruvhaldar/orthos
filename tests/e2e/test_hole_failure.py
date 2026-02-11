import orthos.holes

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
