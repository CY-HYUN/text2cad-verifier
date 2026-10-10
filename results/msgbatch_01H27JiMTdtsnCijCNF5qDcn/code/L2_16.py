import cadquery as cq
import math

sphere = cq.Workplane("XY").sphere(25)

def cyl(direction, r, start, length):
    return cq.Workplane("XY").add(
        cq.Solid.makeCylinder(r, length, cq.Vector(*[d*start for d in direction]), cq.Vector(*direction))
    )

body = sphere
for d in [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0)]:
    body = body.union(cyl(d, 15, 0, 45))

# through holes along X and Y
hx = cq.Workplane("XY").add(cq.Solid.makeCylinder(10, 100, cq.Vector(-50,0,0), cq.Vector(1,0,0)))
hy = cq.Workplane("XY").add(cq.Solid.makeCylinder(10, 100, cq.Vector(0,-50,0), cq.Vector(0,1,0)))
body = body.cut(hx).cut(hy)

# flat platform on top, diameter 20
zc = math.sqrt(25**2 - 10**2)
cutter = cq.Workplane("XY").box(200, 200, 50, centered=(True, True, False)).translate((0, 0, zc))
body = body.cut(cutter)

result = body
