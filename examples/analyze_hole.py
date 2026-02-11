import orthos.holes

laminate_strength = 1000e6 # 1000 MPa
hole_radius = 0.005 # 5mm
characteristic_distance = 0.001 # 1mm (d0)

print("Predicting notched strength...")
predicted_strength = orthos.holes.predict_strength_psc(
    laminate_strength, hole_radius, characteristic_distance
)

print(f"Unnotched Strength: {laminate_strength/1e6} MPa")
print(f"Predicted Notched Strength (PSC): {predicted_strength/1e6:.2f} MPa")
