import cadquery as cq

r = 20
L = 100
cx = cq.Solid.makeCylinder(r, L, cq.Vector(-L/2, 0, 0), cq.Vector(1, 0, 0))
cy = cq.Solid.makeCylinder(r, L, cq.Vector(0, -L/2, 0), cq.Vector(0, 1, 0))
body = cq.Workplane("XY").add(cx).union(cq.Workplane("XY").add(cy))

result = body.faces("%PLANE").shell(-2)
