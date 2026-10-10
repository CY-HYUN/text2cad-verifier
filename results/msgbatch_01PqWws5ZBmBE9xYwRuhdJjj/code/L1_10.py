import cadquery as cq

# Create a rectangular prism base: 100mm long, 50mm wide, 30mm tall
result = cq.Workplane("XY").box(100.0, 50.0, 30.0)

# Add a slot on the top surface
# The slot is 20mm wide, 100mm long, centered on the top surface
# Cut down 15mm from the top
result = result.faces(">Z").workplane().box(100.0, 20.0, 15.0, centered=True, combine="cut")
