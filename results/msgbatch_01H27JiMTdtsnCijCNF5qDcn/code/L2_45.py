import cadquery as cq
import math

# Corrugated pipe: wall profile revolved about the X axis
L = 100.0
period = 10.0
r_mean = 20.0
amp = 2.5
t = 2.0

def wave_r(x):
    return r_mean + amp * math.sin(2 * math.pi * x / period)

def mkwire(ybot):
    x0, x1 = -10.0, 110.0
    pts = [(float(x), wave_r(x)) for x in range(int(x0), int(x1) + 1)]
    w = (cq.Workplane("XY")
         .moveTo(x0, ybot)
         .lineTo(pts[0][0], pts[0][1])
         .spline(pts[1:], includeCurrent=True)
         .lineTo(x1, ybot)
         .close())
    return w.val()

outer_wire = mkwire(10.0)
big_wire = mkwire(-30.0)
inner_wire = big_wire.offset2D(-t)[0]  # offset 2 mm inward

A = cq.Face.makeFromWires(outer_wire)
B = cq.Face.makeFromWires(inner_wire)

rect_pts = [cq.Vector(0, 5, 0), cq.Vector(L, 5, 0), cq.Vector(L, 30, 0),
            cq.Vector(0, 30, 0), cq.Vector(0, 5, 0)]
R = cq.Face.makeFromWires(cq.Wire.makePolygon(rect_pts))

section = A.cut(B).intersect(R)
face = section.Faces()[0]
wire = face.outerWire()

wp = cq.Workplane("XY")
wp.ctx.pendingWires.append(wire)
result = wp.revolve(360, (0, 0, 0), (1, 0, 0))
