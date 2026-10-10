import cadquery as cq
import math

size = 60.0
d = 20.0
r = d / 2.0

# Cube centered at origin
cube = cq.Workplane("XY").box(size, size, size)

# Through-hole along X-axis, axis at Z = +5 (Y = 0)
hole_x = (
    cq.Workplane("YZ")
    .workplane(offset=-size / 2.0 - 1)
    .center(0, 5)
    .circle(r)
    .extrude(size + 2)
)

# Through-hole along Y-axis, axis at Z = -5 (X = 0)
hole_y = (
    cq.Workplane("XZ")
    .workplane(offset=-size / 2.0 - 1)
    .center(0, -5)
    .circle(r)
    .extrude(size + 2)
)

result = cube.cut(hole_x).cut(hole_y)
