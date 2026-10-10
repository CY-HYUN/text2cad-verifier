import cadquery as cq
import math

# Create a disk with a 100mm diameter and 12mm height
result = cq.Workplane("XY").circle(50.0).extrude(12.0)

# Create a sketch on the top face for the holes
sketch = cq.Workplane("XY").workplane(offset=12.0)

# Draw a construction circle with radius 35.0
sketch = sketch.circle(35.0, forConstruction=True)

# Place four points aligned with X/Y axes on the construction circle (at 90° intervals)
# Points at: (35, 0), (0, 35), (-35, 0), (0, -35)
points = [
    (35.0, 0.0),
    (0.0, 35.0),
    (-35.0, 0.0),
    (0.0, -35.0)
]

# Draw circles at each point with diameter 10.0 (radius 5.0)
for point in points:
    sketch = sketch.center(point[0], point[1]).circle(5.0).center(-point[0], -point[1])

# Extrude the sketch downward to cut through
holes = sketch.extrude(-12.0)

# Cut the holes through the disk
result = result.cut(holes)

# Chamfer the circular edges of the holes on the top face
# Select the small circular edges created by the holes
top_edges = result.edges(">Z")
small_edges = top_edges.filter(lambda e: e.Length < 35)
result = result.chamfer(0.8, small_edges)

result = result
