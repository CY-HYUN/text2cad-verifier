import cadquery as cq

size = 60.0
d = 20.0

cube = cq.Workplane("XY").box(size, size, size)

# Hole along X axis at Z=+5 (right view plane = YZ)
hole_x = (
    cq.Workplane("YZ")
    .center(0, 5)
    .circle(d / 2)
    .extrude(size, both=True)
)

# Hole along Y axis at Z=-5 (front view plane = XZ)
hole_y = (
    cq.Workplane("XZ")
    .center(0, -5)
    .circle(d / 2)
    .extrude(size, both=True)
)

result = cube.cut(hole_x).cut(hole_y)
