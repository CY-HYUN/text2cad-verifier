import cadquery as cq

# Create a new workplane on the XY plane at the origin
wp = cq.Workplane("XY")

# Draw a right triangle with legs along X and Y axes
# Vertices: (0,0), (30,0), (0,40), back to (0,0)
triangle = wp.polyline([(0, 0), (30, 0), (0, 40), (0, 0)]).close()

# Extrude the triangle 60 mm upward along the Z-axis
result = triangle.extrude(60.0)
