import cadquery as cq

blank = cq.Workplane("XY").box(80, 60, 30, centered=(True, True, False))
notch = cq.Workplane("XY").box(50, 30, 20, centered=False).translate((-10, 0, 10))
result = blank.cut(notch)

result = result.edges(cq.selectors.BoxSelector((-11, -1, 9), (-9, 1, 31))).edges("|Z").fillet(4)
