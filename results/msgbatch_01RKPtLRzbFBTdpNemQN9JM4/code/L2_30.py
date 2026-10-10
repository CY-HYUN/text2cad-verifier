import cadquery as cq

body = cq.Workplane("XY").box(60, 30, 30, centered=(True, True, False))

arch = (
    cq.Workplane("YZ")
    .circle(10)
    .extrude(30, both=True)
)
result = body.cut(arch)

holes = (
    cq.Workplane("XY")
    .pushPoints([(-15, 0), (15, 0)])
    .circle(3)
    .extrude(30)
)
result = result.cut(holes)
