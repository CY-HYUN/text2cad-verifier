import cadquery as cq

# Base plate 100x100x10, bottom at z=0, top at z=10
plate = cq.Workplane("XY").box(100, 100, 10, centered=(True, True, False))

# Sphere R20 centered on the top surface center (merged)
sphere = cq.Workplane("XY").sphere(20).translate((0, 0, 10))
body = plate.union(sphere)

# Cut everything protruding below the bottom face (z < 0)
cutter = (
    cq.Workplane("XY")
    .rect(150, 150)
    .extrude(-30)
)
result = body.cut(cutter)
