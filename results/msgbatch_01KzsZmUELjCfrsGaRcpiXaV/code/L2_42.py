import cadquery as cq
import math

# Create the two rectangular plates
# Horizontal plate: 100x60x10mm
horizontal_plate = cq.Workplane("XY").box(100, 60, 10)

# Vertical plate: 100x60x10mm, positioned perpendicular to horizontal plate
# Shift it up by 10mm (half thickness of horizontal) so they join at the corner
vertical_plate = cq.Workplane("XY").box(60, 100, 10).translate((0, 0, 10))

# Combine the two plates
bracket = horizontal_plate.union(vertical_plate)

# Create the triangular reinforcement
# Right-angled triangle with 50mm legs, 10mm thick
# Triangle vertices for a right triangle with legs of 50mm
triangle_points = [
    (0, 0),
    (50, 0),
    (0, 50),
]

# Create the triangular profile and extrude it
triangle_sketch = cq.Workplane("XY").polyline(triangle_points).close()
triangle_3d = triangle_sketch.extrude(10)

# Position the triangle at the inner corner of the L-shape
triangle_reinforcement = triangle_3d.translate((0, 0, 0))

# Union the triangle with the bracket
bracket = bracket.union(triangle_reinforcement)

# Create through-holes in both plates
# Horizontal plate hole: diameter 20mm, centered on the horizontal plate
# Center of horizontal plate is at (0, 0, 5)
hole_horizontal = cq.Workplane("Z").circle(10).extrude(-10, both=True).translate((0, 0, 5))

# Vertical plate hole: diameter 20mm, centered on the vertical plate
# Center of vertical plate is at (0, 0, 15) (since it's at z offset of 10, and extends 100mm in y with center at 0)
hole_vertical = cq.Workplane("Z").circle(10).extrude(-10, both=True).translate((0, 0, 15))

# Cut the holes from the bracket
result = bracket.cut(hole_horizontal).cut(hole_vertical)
