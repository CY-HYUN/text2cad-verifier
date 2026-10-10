import cadquery as cq
import math

# Start with a new part - create a cylinder
# Circle with diameter 40mm on XY plane, extruded 40mm in Z direction
cylinder = cq.Workplane("XY").circle(20).extrude(40)

# Create the conical pit
# Switch to XZ plane to draw the triangular profile
# The triangle has:
# - Base at the top (y=0) with radius 15mm (from origin at x=15, z=40)
# - Apex at the bottom (y=0) at x=0, z=25 (which is 15mm depth from z=40)

# Create a workplane on XZ plane
xz_plane = cq.Workplane("XZ")

# Draw the triangular profile for revolution
# Points: (15, 40) at top, (0, 25) at apex, (0, 40) closing the triangle
triangle = xz_plane.polyline([(15, 40), (0, 25), (0, 40)]).close()

# Revolve 360 degrees around the Z-axis to create the cone
cone_cut = triangle.revolve(360, axis=(0, 0, 1))

# Perform a cut operation - subtract the cone from the cylinder
result = cylinder.cut(cone_cut)
