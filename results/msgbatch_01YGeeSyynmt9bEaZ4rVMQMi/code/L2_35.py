import cadquery as cq

size = 60.0
d = 20.0

# Base cube centered at origin
cube = cq.Workplane("XY").box(size, size, size)

# Hole along X-axis (right view plane = YZ), axis at Z=+5
hole_x = (
    cq.Workplane("YZ")
    .center(0, 5)
    .circle(d / 2)
    .extrude(size, both=True)
)

# Hole along Y-axis (front view plane = XZ), axis at Z=-5
hole_y = (
    cq.Workplane("XZ")
    .center(0, -5)
    .circle(d / 2)
    .extrude(size, both=True)
)

# Both cuts intersect internally, forming a combined cavity
result = cube.cut(hole_x).cut(hole_y)
