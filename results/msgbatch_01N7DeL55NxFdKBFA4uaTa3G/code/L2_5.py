import cadquery as cq
import math

R = 10.0      # outer radius (20 mm diameter)
t = 2.0       # wall thickness
Ri = R - t
L_main = 50.0
L_br = 50.0
half = math.radians(30)  # 60 degrees between branches

J = cq.Vector(0, 0, L_main)
d_main = cq.Vector(0, 0, 1)
d_b1 = cq.Vector(math.sin(half), 0, math.cos(half))
d_b2 = cq.Vector(-math.sin(half), 0, math.cos(half))

def swept_tube(r, start, d, L, x_dir):
    end = start + d * L
    path = cq.Wire.assembleEdges([cq.Edge.makeLine(start, end)])
    plane = cq.Plane(origin=start, xDir=x_dir, normal=d)
    return cq.Workplane(plane).circle(r).sweep(cq.Workplane().add(path))

# Outer body: swept along the three path segments, smooth merge with sphere at the junction
outer = (
    swept_tube(R, cq.Vector(0, 0, 0), d_main, L_main, cq.Vector(1, 0, 0))
    .union(swept_tube(R, J, d_b1, L_br, cq.Vector(0, 1, 0)))
    .union(swept_tube(R, J, d_b2, L_br, cq.Vector(0, 1, 0)))
    .union(cq.Workplane().add(cq.Solid.makeSphere(R, J, angleDegrees1=-90, angleDegrees2=90)))
)

# Inner cavity (equivalent to shell with three end faces removed), extended past open ends
ext = 1.0
inner = (
    swept_tube(Ri, cq.Vector(0, 0, -ext), d_main, L_main + ext, cq.Vector(1, 0, 0))
    .union(swept_tube(Ri, J, d_b1, L_br + ext, cq.Vector(0, 1, 0)))
    .union(swept_tube(Ri, J, d_b2, L_br + ext, cq.Vector(0, 1, 0)))
    .union(cq.Workplane().add(cq.Solid.makeSphere(Ri, J, angleDegrees1=-90, angleDegrees2=90)))
)

result = outer.cut(inner)
