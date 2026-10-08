import cadquery as cq
import math

# Base disc
base = cq.Workplane("XY").circle(60.0).extrude(10.0)

# Spiral centerline r = 5 + 3t, t in [0, 3*pi]
N = 80
t0, t1 = 0.0, 3 * math.pi
half_w = 2.0

def pt(t):
    r = 5 + 3 * t
    return (r * math.cos(t), r * math.sin(t))

def tangent(t):
    r = 5 + 3 * t
    dx = 3 * math.cos(t) - r * math.sin(t)
    dy = 3 * math.sin(t) + r * math.cos(t)
    L = math.hypot(dx, dy)
    return (dx / L, dy / L)

outer, inner = [], []
for i in range(N + 1):
    t = t0 + (t1 - t0) * i / N
    x, y = pt(t)
    tx, ty = tangent(t)
    nx, ny = ty, -tx
    outer.append((x + half_w * nx, y + half_w * ny))
    inner.append((x - half_w * nx, y - half_w * ny))

# Cap midpoints
pe = pt(t1); te = tangent(t1)
end_mid = (pe[0] + half_w * te[0], pe[1] + half_w * te[1])
ps = pt(t0); ts = tangent(t0)
start_mid = (ps[0] - half_w * ts[0], ps[1] - half_w * ts[1])

inner_rev = inner[::-1]

wall = (
    cq.Workplane("XY").workplane(offset=10.0)
    .moveTo(*outer[0])
    .spline(outer[1:], includeCurrent=True)
    .threePointArc(end_mid, inner_rev[0])
    .spline(inner_rev[1:], includeCurrent=True)
    .threePointArc(start_mid, outer[0])
    .close()
    .extrude(25.0)
)

# Chamfer top edges of vortex wall
try:
    wall = wall.faces(">Z").edges().chamfer(0.5)
except Exception:
    pass

result = base.union(wall)

# Exhaust port through the base (and wall start)
hole = cq.Workplane("XY").workplane(offset=-1).circle(4.0).extrude(40.0)
result = result.cut(hole)
