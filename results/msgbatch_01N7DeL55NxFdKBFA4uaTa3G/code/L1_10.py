import cadquery as cq

base = cq.Workplane("XY").rect(100.0, 50.0).extrude(30.0)

slot = (
    cq.Workplane("XY", origin=(0, 0, 30.0 - 15.0))
    .rect(100.0, 20.0)
    .extrude(15.0)
)

result = base.cut(slot)
