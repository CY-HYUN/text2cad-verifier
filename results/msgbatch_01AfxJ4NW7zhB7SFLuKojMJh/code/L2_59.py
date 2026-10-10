import cadquery as cq

cube = cq.Workplane("XY").box(50, 50, 50)

# Blind hole along X, entering from the +X face, 30 deep (x from 25 down to -5)
hole_x = (
    cq.Workplane("YZ")
    .workplane(offset=-5)
    .circle(7.5)
    .extrude(30)
)

# Blind hole along Z, entering from the +Z face, 30 deep (z from 25 down to -5)
hole_z = (
    cq.Workplane("XY")
    .workplane(offset=-5)
    .circle(7.5)
    .extrude(30)
)

result = cube.cut(hole_x).cut(hole_z)
