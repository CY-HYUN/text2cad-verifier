import cadquery as cq

# Create a new workplane with the XY plane as the base sketch plane
workplane = cq.Workplane("XY")

# Draw a rectangular plate (120.0 mm long and 40.0 mm wide) and extrude it by 10.0 mm
plate = workplane.box(120.0, 40.0, 10.0, centered=True)

# Get the top surface of the plate to sketch the holes
top_face = plate.faces(">Z").workplane()

# Create a sketch on the top surface with two circular holes
# Hole diameter is 10.0 mm (radius 5.0 mm)
# Hole centers are along the length centerline, each 20.0 mm from the left and right ends
# Length is 120.0 mm, so hole centers are at:
# Left hole: x = -120.0/2 + 20.0 = -40.0 mm
# Right hole: x = 120.0/2 - 20.0 = 40.0 mm
# Both holes are on the centerline (y = 0)

sketch = top_face.circle(5.0).moveTo(-40.0, 0).circle(5.0).moveTo(40.0, 0)

# Perform an extruded cut through the entire thickness (10.0 mm)
result = plate.cutThruAll(sketch)
