import cadquery as cq
import math

# Create a 40mm cube
cube = cq.Workplane("XY").box(40, 40, 40)

# Cut a through-hole with diameter 30mm at the center
hole = cq.Workplane("XY").cylinder(height=40, radius=15, centered=True)
cube = cube.cut(hole)

# Select the four vertical edges and apply chamfer
# Get all edges of the cube
edges = cube.edges()

# Filter for vertical edges (edges parallel to Z-axis)
# Vertical edges have start and end points with same X,Y but different Z
vertical_edges = [edge for edge in edges if abs(edge.startPoint.x - edge.endPoint.x) < 0.01 and 
                                            abs(edge.startPoint.y - edge.endPoint.y) < 0.01]

# Apply chamfer to the four vertical edges
# We need to select them properly using the edges selector
cube = cube.edges("|Z").chamfer(10)

result = cube
