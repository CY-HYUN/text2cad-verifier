import cadquery as cq

plate = cq.Workplane("XY").box(120, 50, 6, centered=(True, True, False))
plate = plate.edges("|Z").fillet(4)
slot = cq.Workplane("XY").slot2D(80, 18, 0).extrude(6)
result = plate.cut(slot)
