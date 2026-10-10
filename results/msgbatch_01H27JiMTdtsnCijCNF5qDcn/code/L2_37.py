import cadquery as cq
import math

result = cq.Workplane("XY").sphere(20)

dirs = [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]

for d in dirs:
    cyl = cq.Solid.makeCylinder(7.5, 30, cq.Vector(0,0,0), cq.Vector(*d))
    result = result.union(cq.Workplane("XY").add(cyl))

for d in dirs:
    start = cq.Vector(d[0]*30, d[1]*30, d[2]*30)
    hole = cq.Solid.makeCylinder(4, 10, start, cq.Vector(-d[0], -d[1], -d[2]))
    result = result.cut(cq.Workplane("XY").add(hole))
