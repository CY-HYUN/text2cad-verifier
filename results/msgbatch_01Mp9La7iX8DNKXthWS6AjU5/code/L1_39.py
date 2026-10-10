import cadquery as cq

rect = cq.Workplane("XY").center(30, 0).rect(60, 40).extrude(10)
semi = (cq.Workplane("XY")
        .moveTo(60, -20)
        .threePointArc((80, 0), (60, 20))
        .close()
        .extrude(10))
result = rect.union(semi)
