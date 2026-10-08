import cadquery as cq

# Base plate 100x100x10, bottom at z=0, top at z=10
plate = cq.Workplane("XY").box(100, 100, 10, centered=(True, True, False))

# Sphere R20 centered at the center of the top surface (0,0,10), merged
sphere = cq.Workplane("XY").sphere(20).translate((0, 0, 10))
body = plate.union(sphere)

# Cut away anything protruding below the bottom surface (z<0)
cutter = (
    cq.Workplane("XY")
    .rect(200, 200)
    .extrude(-50)
)
result = body.cut(cutter)
