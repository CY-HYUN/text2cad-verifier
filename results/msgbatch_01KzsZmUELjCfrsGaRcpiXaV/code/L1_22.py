import cadquery as cq
import math

# Create the frustum by lofting between bottom and top squares
# Bottom square: 60x60 centered at origin, z=0
# Top square: 40x40 centered at origin, z=30

# Create bottom square profile
bottom_points = [
    (-30, -30),
    (30, -30),
    (30, 30),
    (-30, 30)
]

# Create top square profile
top_points = [
    (-20, -20),
    (20, -20),
    (20, 20),
    (-20, 20)
]

# Build the frustum using loft
result = (
    cq.Workplane("XY")
    .polyline(bottom_points)
    .close()
    .workplane(offset=30)
    .polyline(top_points)
    .close()
    .loft(ruled=True)
)

# Create a cylindrical hole with diameter 20mm (radius 10mm) through the center
hole = cq.Workplane("XY").circle(10).extrude(35, both=True)

# Cut the hole from the frustum
result = result.cut(hole)
