import cadquery as cq

block = cq.Workplane("XY").box(100.0, 50.0, 30.0, centered=(True, True, False))
slot = (cq.Workplane("XY").workplane(offset=10.0)
        .rect(100.0, 30.0).extrude(20.0))
result = block.cut(slot)
