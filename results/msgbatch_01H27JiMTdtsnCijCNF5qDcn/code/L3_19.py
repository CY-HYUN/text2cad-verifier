import cadquery as cq
import math

# Base disc with central exhaust port (cut from base only)
base = cq.Workplane("XY").circle(60.0).extrude(10.0)
base = base.cut(cq.Workplane("XY").circle(4.0).extrude(10.0))

# Spiral centerline and offsets
N = 90
T = 3 * math.pi
w = 2.0
left, right = [], []
def center(t):
    r = 5 + 3 * t
    return r * math.cos(t), r * math.sin(t)
def tangent(t):
    r = 5 + 3 * t
    tx = 3 * math.cos(t) - r * math.sin(t)
    ty = 3 * math.sin(t) + r * math.cos(t)
    l = math.hypot(tx, ty)
    return tx / l, ty / l
for i in range(N + 1):
    t = T * i / N
    x, y = center(t)
    tx, ty = tangent(t)
    nx, ny = ty, -tx
    left.append((x + w * nx, y + w * ny))
    right.append((x - w * nx, y - w * ny))

# End cap arc midpoints
sx, sy = center(0)
stx, sty = tangent(0)
start_mid = (sx - w * stx, sy - w * sty)
ex, ey = center(T)
etx, ety = tangent(T)
end_mid = (ex + w * etx, ey + w * ety)

wall = (
    cq.Workplane("XY").workplane(offset=10.0)
    .moveTo(*left[0])
    .spline(left[1:], includeCurrent=True)
    .threePointArc(end_mid, right[-1])
    .spline(right[::-1][1:], includeCurrent=True)
    .threePointArc(start_mid, left[0])
    .close()
    .extrude(25.0)
)

# Chamfer top edges of the vortex wall
wall = wall.faces(">Z").chamfer(0.5)

result = base.union(wall)
