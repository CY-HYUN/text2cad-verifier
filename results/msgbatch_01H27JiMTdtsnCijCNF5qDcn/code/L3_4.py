import cadquery as cq

# Four sections on YZ-parallel planes at X = 0, 50, 100, 150 (centred on the X axis)
solid = (
    cq.Workplane("YZ")
    .circle(7.5)
    .workplane(offset=50)
    .ellipse(12.5, 10)
    .workplane(offset=50)
    .ellipse(11, 9)
    .workplane(offset=50)
    .circle(10)
    .loft(ruled=False, combine=True)
)

# Shell: remove both end faces, 1.5 mm wall thickness (inward)
result = solid.faces("<X or >X").shell(-1.5)
