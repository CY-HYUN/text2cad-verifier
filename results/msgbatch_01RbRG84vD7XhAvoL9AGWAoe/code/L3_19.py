import cadquery as cq
import math

# Parameters
base_d = 120.0
base_t = 10.0
wall_h = 25.0
wall_t = 4.0
hole_d = 8.0
a, b = 20.0, 3.5
th0, th1 = 0.0, 3 * math.pi
N = 160
half = wall_t / 2.0

def pt(th):
    r = a + b * th
    return (r * math.cos(th), r * math.sin(th))

def tangent(th):
    r = a + b * th
    dx = b * math.cos(th) - r * math.sin(th)
    dy = b * math.sin(th) + r * math.cos(th)
    L = math.hypot(dx, dy)
    return (dx / L, dy / L)

outer, inner = [], []
for i in range(N + 1):
    th = th0 + (th1 - th0) * i / N
    x, y = pt(th)
    tx, ty = tangent(th)
    nx, ny = ty, -tx  # outward normal (spiral grows CCW)
    outer.append(cq.Vector(x + half * nx, y + half * ny, base_t))
    inner.append(cq.Vector(x - half * nx, y - half * ny, base_t))

# End caps (R2 rounded ends)
xe, ye = pt(th1); txe, tye = tangent(th1)
end_mid = cq.Vector(xe + half * txe, ye + half * tye, base_t)
xs, ys = pt(th0); txs, tys = tangent(th0)
start_mid = cq.Vector(xs - half * txs, ys - half * tys, base_t)

e1 = cq.Edge.makeSpline(outer)
e2 = cq.Edge.makeThreePointArc(outer[-1], end_mid, inner[-1])
e3 = cq.Edge.makeSpline(list(reversed(inner)))
e4 = cq.Edge.makeThreePointArc(inner[0], start_mid, outer[0])

wire = cq.Wire.assembleEdges([e1, e2, e3, e4])
face = cq.Face.makeFromWires(wire)
wall = cq.Solid.extrudeLinear(face, cq.Vector(0, 0, wall_h))

base = cq.Workplane("XY").circle(base_d / 2).extrude(base_t)
result = base.union(cq.Workplane("XY").add(wall))

# Central discharge hole
hole = cq.Workplane("XY").circle(hole_d / 2).extrude(base_t + wall_h + 1).translate((0, 0, -0.5))
result = result.cut(hole)
