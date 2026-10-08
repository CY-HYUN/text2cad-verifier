import cadquery as cq

base = cq.Workplane("XY").box(60.0, 60.0, 10.0, centered=(True, True, False))
pillar = (
    cq.Workplane("XY")
    .workplane(offset=10.0)
    .circle(15.0)
    .extrude(50.0)
)
result = base.union(pillar)
