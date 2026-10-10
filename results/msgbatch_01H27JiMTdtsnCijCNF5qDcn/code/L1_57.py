import cadquery as cq

blank = cq.Workplane("XY").rect(80.0, 60.0).extrude(30.0)

notch = (cq.Workplane("XY").workplane(offset=10.0)
         .center(15.0, 15.0).rect(50.0, 30.0).extrude(20.0))

result = blank.cut(notch)

result = result.edges(cq.selectors.BoxSelector((-11, -1, 9), (-9, 1, 31))).edges("|Z").fillet(4.0)
