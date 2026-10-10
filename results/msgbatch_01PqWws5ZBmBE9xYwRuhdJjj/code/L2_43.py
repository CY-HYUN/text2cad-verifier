import cadquery as cq
import math

# Create the base square 60x60 mm and extrude by 20 mm
base = cq.Workplane("XY").box(60, 60, 20, centered=True)

# Get the top face to work on
top_face = base.faces(">Z").val()

# Create a workplane on the top face
wp_top = cq.Workplane("XY").workplaneFromFace(top_face)

# Draw a centered square with side length 40 mm and cut through
# This creates a frame by cutting a square hole through the top
frame = wp_top.box(40, 40, 20, centered=True, combine=False)
result = base.cut(frame)

# Now add the cylinder on top
# Create a workplane on the new top face after the cut
top_face_after_cut = result.faces(">Z").val()
wp_cylinder = cq.Workplane("XY").workplaneFromFace(top_face_after_cut)

# Draw a centered circle with diameter 40 mm (radius 20 mm) and extrude by 20 mm
cylinder = wp_cylinder.circle(20).extrude(20)

# Merge the cylinder with the frame structure
result = result.union(cylinder)
