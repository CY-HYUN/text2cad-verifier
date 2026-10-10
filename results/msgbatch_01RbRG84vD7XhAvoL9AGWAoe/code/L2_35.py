import cadquery as cq

L = 60.0
r = 10.0

cube = cq.Workplane("XY").box(L, L, L)

hole_x = (
    cq.Workplane("YZ")
    .workplane(offset=-L)
    .center(0, 5)
    .circle(r)
    .extrude(2 * L)
)

hole_y = (
    cq.Workplane("XZ")
    .workplane(offset=-L)
    .center(0, -5)
    .circle(r)
    .extrude(2 * L)
)

result = cube.cut(hole_x).cut(hole_y)
