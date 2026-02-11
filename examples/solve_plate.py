from orthos.plate import RectangularPlate

# Define a [0/90]s Laminate Plate (1m x 1m)
# Assuming typical Carbon/Epoxy properties as default
plate = RectangularPlate(length=1.0, width=1.0, layup=[0, 90], sym=True)

# Apply Distributed Load q0 = 1000 Pa
print("Solving plate bending...")
deflection = plate.solve_bending(load=1000, method='navier')

print(f"Max deflection: {deflection.max()} m")
plate.plot_surface(deflection)
