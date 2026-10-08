import cadquery as cq
import math

# Base disc
base = cq.Workplane("XY").circle(60.0).extrude(10.0)

# Spiral centerline r = 5 + 3t, t in [0, 3*pi]
N = 120
t_end = 3 * math.pi
z0 = 10.0
half_w = 2.0

def pt(t):
    r = 5 + 3 * t
    return r * math.cos(t), r * math.sin(t)

def tan_norm(t):
    r = 5 + 3 * t
    dx = 3 * math.cos(t) - r * math.sin(t)
    dy = 3 * math.sin(t) + r * math.cos(t)
    L = math.hypot(dx, dy)
    tx, ty = dx / L, dy / L
    return (tx, ty), (ty, -tx)  # normal points outward

outer = []
inner = []
for i in range(N + 1):
    t = t_end * i / N
    x, y = pt(t)
    _, (nx, ny) = tan_norm(t)
    outer.append(cq.Vector(x + half_w * nx, y + half_w * ny, z0))
    inner.append(cq.Vector(x - half_w * nx, y - half_w * ny, z0))

e_outer = cq.Edge.makeSpline(outer)
e_inner = cq.Edge.makeSpline(list(reversed(inner)))

# End cap arc
xe, ye = pt(t_end)
(tx, ty), _ = tan_norm(t_end)
cap_end = cq.Edge.makeThreePointArc(
    outer[-1], cq.Vector(xe + half_w * tx, ye + half_w * ty, z0), inner[-1])

# Start cap arc
xs, ys = pt(0)
(tx0, ty0), _ = tan_norm(0)
cap_start = cq.Edge.makeThreePointArc(
    inner[0], cq.Vector(xs - half_w * tx0, ys - half_w * ty0, z0), outer[0])

wire = cq.Wire.assembleEdges([e_outer, cap_end, e_inner, cap_start])
face = cq.Face.makeFromWires(wire)
wall = cq.Solid.extrudeLinear(face, cq.Vector(0, 0, 25.0))

result = base.union(cq.Workplane("XY").add(wall))

# Exhaust port through the base
hole = cq.Workplane("XY").circle(4.0).extrude(10.0)
result = result.cut(hole)

# Chamfer top edge of vortex wall
try:
    result = result.faces(">Z").edges().chamfer(0.5)
except Exception:
    pass
