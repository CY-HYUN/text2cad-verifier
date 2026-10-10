import cadquery as cq
import math

# Base disc
base = cq.Workplane("XY").circle(60.0).extrude(10.0)

# Spiral centerline and offset curves
def P(t):
    r = 5 + 3 * t
    return (r * math.cos(t), r * math.sin(t))

def T(t):
    r = 5 + 3 * t
    dx = 3 * math.cos(t) - r * math.sin(t)
    dy = 3 * math.sin(t) + r * math.cos(t)
    l = math.hypot(dx, dy)
    return (dx / l, dy / l)

n = 80
tmax = 3 * math.pi
ts = [tmax * i / n for i in range(n + 1)]
w = 2.0
A, B = [], []
for t in ts:
    px, py = P(t)
    tx, ty = T(t)
    nx, ny = -ty, tx
    A.append((px + w * nx, py + w * ny))
    B.append((px - w * nx, py - w * ny))

p0 = P(0)
t0 = T(0)
pe = P(tmax)
te = T(tmax)
cap_end = (pe[0] + w * te[0], pe[1] + w * te[1])
cap_start = (p0[0] - w * t0[0], p0[1] - w * t0[1])

wall = (
    cq.Workplane("XY").workplane(offset=10.0)
    .moveTo(*A[0])
    .spline(A[1:], includeCurrent=True)
    .threePointArc(cap_end, B[-1])
    .spline(B[::-1][1:], includeCurrent=True)
    .threePointArc(cap_start, A[0])
    .close()
    .extrude(25.0)
)

# Chamfer top edge of the vortex wall
wall = wall.faces(">Z").chamfer(0.5)

result = base.union(wall)

# Central exhaust port through the base
hole = cq.Workplane("XY").circle(4.0).extrude(10.0)
result = result.cut(hole)
