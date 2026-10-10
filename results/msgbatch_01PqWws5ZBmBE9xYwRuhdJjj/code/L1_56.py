import cadquery as cq
import math

# Create the blank: 80x80 square base extruded by 45
base = cq.Workplane("XY").rect(80.0, 80.0).extrude(45.0)

# Create the frustum by lofting from bottom square to top smaller square
# First, create a sketch on the top surface for the 50x50 square
bottom_sketch = cq.Workplane("XY").rect(80.0, 80.0)
top_sketch = cq.Workplane("XY").offset(45.0).rect(50.0, 50.0)

# Use loft to create frustum shape
# We'll create this by making the base and then adding a tapered section
frustum_base = cq.Workplane("XY").rect(80.0, 80.0).extrude(45.0)

# Create a top section with 50x50 square and loft between them
# Using a different approach: create the full frustum shape
top_face = frustum_base.faces(">Z").workplane()
top_square = top_face.rect(50.0, 50.0)

# Create frustum by sketching and lofting
sketch_bottom = cq.Sketch().rect(80.0, 80.0)
sketch_top = cq.Sketch().rect(50.0, 50.0)

# Build frustum using rect extrude with taper
frustum = cq.Workplane("XY").rect(80.0, 80.0).extrude(45.0, taper=math.atan2(80.0 - 50.0, 2 * 45.0) * 180 / math.pi)

# Now create the cavity: select top surface and draw centered 30x30 square
cavity_workplane = frustum.faces(">Z").workplane()
cavity_sketch = cavity_workplane.rect(30.0, 30.0)
frustum_with_cavity = cavity_sketch.extrude(-15.0, combine=False)

# Combine base with cavity cut
result = frustum.cut(cq.Workplane("XY").rect(30.0, 30.0).extrude(-15.0))

# Apply 45° chamfer to the edges of the cavity opening
# Get the top face and find the edges of the cavity
top_surface = result.faces(">Z")
result = result.edges("|Z").chamfer(1.0)

# Ensure the cavity opening edges are chamfered
cavity_edges = result.edges("<<Z[0]").filter(lambda e: e.geomType() == "CIRCLE" or (hasattr(e, "Length") and e.Length < 50))
result = result.edges(lambda e: (abs(e.startPoint.z - 30.0) < 0.1 or abs(e.endPoint.z - 30.0) < 0.1)).chamfer(1.0)

# Final result with all features
result = frustum.cut(cq.Workplane("XY").workplane(offset=45.0).rect(30.0, 30.0).extrude(-15.0)).edges("|Z").chamfer(1.0)
