import cadquery as cq

base = 60.0
top = 40.0
h = 30.0
hole_d = 20.0

body = (
    cq.Workplane("XY")
    .rect(base, base)
    .workplane(offset=h)
    .rect(top, top)
    .loft(combine=True)
)

hole = cq.Workplane("XY").circle(hole_d / 2).extrude(h)

result = body.cut(hole)
