import cadquery as cq

cube = cq.Workplane("XY").box(60, 60, 60)

# Hole along X axis, circle at Y=0, Z=5 (on the right/YZ plane)
cyl_x = cq.Workplane("XY").add(
    cq.Solid.makeCylinder(10, 100, cq.Vector(-50, 0, 5), cq.Vector(1, 0, 0))
)

# Hole along Y axis, circle at X=0, Z=-5 (on the front/XZ plane)
cyl_y = cq.Workplane("XY").add(
    cq.Solid.makeCylinder(10, 100, cq.Vector(0, -50, -5), cq.Vector(0, 1, 0))
)

result = cube.cut(cyl_x).cut(cyl_y)
