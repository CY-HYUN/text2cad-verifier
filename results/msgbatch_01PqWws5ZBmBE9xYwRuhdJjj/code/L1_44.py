import cadquery as cq

# Create the base cube
result = cq.Workplane("XY").box(40.0, 40.0, 40.0)

# Select the top face to add holes
result = result.faces(">Z").workplane()

# Add the through hole (diameter 20.0 mm)
result = result.hole(20.0, 40.0)

# Select the top face again for counterbore
result = result.faces(">Z").workplane()

# Add the counterbore (diameter 30.0 mm, depth 10.0 mm)
result = result.counterbore(30.0, 10.0, 20.0)

# Return to the 3D solid
result = result.cutThruAll()
