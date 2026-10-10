import cadquery as cq
import math

R_out = 10.0
R_in = 8.0
L_main = 60.0
L_branch = 60.0
half = math.radians(30)

d1 = cq.Vector(math.sin(half), 0, math.cos(half))
d2 = cq.Vector(-math.sin(half), 0, math.cos(half))
origin = cq.Vector(0, 0, 0)

def body(r, extra=0.0):
    main = cq.Solid.makeCylinder(r, L_main + extra, cq.Vector(0, 0, -L_main - extra), cq.Vector(0, 0, 1))
    b1 = cq.Solid.makeCylinder(r, L_branch + extra, origin, d1)
    b2 = cq.Solid.makeCylinder(r, L_branch + extra, origin, d2)
    sph = cq.Solid.makeSphere(r, origin, cq.Vector(0, 0, 1), -90, 90, 360)
    w = cq.Workplane("XY").add(main).union(cq.Workplane("XY").add(b1)).union(cq.Workplane("XY").add(b2)).union(cq.Workplane("XY").add(sph))
    return w

outer = body(R_out)
inner = body(R_in, extra=1.0)

result = outer.cut(inner)
