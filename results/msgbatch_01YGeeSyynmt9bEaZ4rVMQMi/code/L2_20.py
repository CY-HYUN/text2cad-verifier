import cadquery as cq
import math

# Cube 50mm (extruded square)
cube = cq.Workplane("XY").rect(50, 50, centered=False).extrude(50)

# Diagonal from (0,0,0) to (50,50,50)
d = cq.Vector(1, 1, 1).normalized()
center = cq.Vector(25, 25, 25)
L = 200.0
start = center - d * (L / 2)

# Circle of dia 10 on plane perpendicular to diagonal, extruded through all
cyl = cq.Solid.makeCylinder(5.0, L, start, d)

result = cube.cut(cq.Workplane("XY").add(cyl))
