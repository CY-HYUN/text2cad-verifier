import cadquery as cq
import math

# Create a disk with a 100mm diameter and 12mm height
result = cq.Workplane("XY").circle(50.0).extrude(12.0)

# Get the top face and select it for sketching
top_face = result.faces(">Z").face0

# Create a sketch on the top face
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

# Cut through the disk with the four holes
result = result.cut(sketch.extrude(12.0, both=True))

# Apply 45° chamfer to the circular edges of the four holes on the top face
# Get the edges of the holes on the top face and chamfer them
for point in points:
    # Select edges near each hole on the top face
    edges_to_chamfer = result.edges().filter(
        lambda e: (
            abs(e.endPoint().x - point[0]) < 10 or abs(e.startPoint().x - point[0]) < 10
        ) and e.endPoint().z > 11.5
    )
    if edges_to_chamfer.size() > 0:
        result = result.chamfer(0.8, edges_to_chamfer)

# Alternative approach: chamfer all top circular edges with the correct radius
result = result.chamfer(0.8, result.edges(">Z").filter(lambda e: e.Length < 50))

result = result
