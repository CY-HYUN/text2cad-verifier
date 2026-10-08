import cadquery as cq

size = 60.0
r = 10.0
L = 100.0  # longer than the cube so holes pass completely through

cube = cq.Solid.makeBox(size, size, size, pnt=cq.Vector(-size / 2, -size / 2, -size / 2))

# Hole along X-axis, axis at Z=+5
cyl_x = cq.Solid.makeCylinder(r, L, pnt=cq.Vector(-L / 2, 0, 5), dir=cq.Vector(1, 0, 0))
# Rotate about its own axis to move the seam away from the intersection region
cyl_x = cyl_x.rotate(cq.Vector(0, 0, 5), cq.Vector(1, 0, 5), 37)

# Hole along Y-axis, axis at Z=-5
cyl_y = cq.Solid.makeCylinder(r, L, pnt=cq.Vector(0, -L / 2, -5), dir=cq.Vector(0, 1, 0))
cyl_y = cyl_y.rotate(cq.Vector(0, 0, -5), cq.Vector(0, 1, -5), 53)

# Combine the hole tools first, then cut once
tools = cyl_x.fuse(cyl_y).clean()
shape = cube.cut(tools)
shape = shape.fix().clean()

result = cq.Workplane("XY").newObject([shape])
