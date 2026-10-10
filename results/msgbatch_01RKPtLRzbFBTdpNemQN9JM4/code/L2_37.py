import cadquery as cq
import math

sphere = cq.Workplane("XY").sphere(20)
body = sphere

dirs = [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]

for d in dirs:
    dv = cq.Vector(*d)
    cyl = cq.Solid.makeCylinder(7.5, 35, dv * 15, dv)
    body = body.union(cq.Workplane("XY").add(cyl))

for d in dirs:
    dv = cq.Vector(*d)
    hole = cq.Solid.makeCylinder(4, 10, dv * 40, dv)
    body = body.cut(cq.Workplane("XY").add(hole))

result = body
