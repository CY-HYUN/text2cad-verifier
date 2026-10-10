import cadquery as cq
import math

base_t = 10.0
wall_h = 25.0
half_t = 2.0

# Base disc with central exhaust hole
base = cq.Workplane("XY").circle(60).extrude(base_t)

def spiral(theta):
    r = 20 + 3.5 * theta
    dr = 3.5
    x = r * math.cos(theta)
    y = r * math.sin(theta)
    tx = dr * math.cos(theta) - r * math.sin(theta)
    ty = dr * math.sin(theta) + r * math.cos(theta)
    l = math.hypot(tx, ty)
    tx /= l
    ty /= l
    nx, ny = ty, -tx
    return x, y, tx, ty, nx, ny

N = 240
tmax = 3 * math.pi
outer = []
inner = []
for i in range(N + 1):
    th = tmax * i / N
    x, y, tx, ty, nx, ny = spiral(th)
    outer.append((x + half_t * nx, y + half_t * ny))
    inner.append((x - half_t * nx, y - half_t * ny))

# Rounded end cap (R2 semicircle)
x, y, tx, ty, nx, ny = spiral(tmax)
cap = []
M = 16
for j in range(1, M):
    phi = math.pi * j / M
    cap.append((x + half_t * (math.cos(phi) * nx + math.sin(phi) * tx),
                y + half_t * (math.cos(phi) * ny + math.sin(phi) * ty)))

pts = outer + cap + inner[::-1]

wall = (cq.Workplane("XY").workplane(offset=base_t)
        .polyline(pts).close().extrude(wall_h))

result = base.union(wall)
hole = cq.Workplane("XY").circle(4).extrude(base_t)
result = result.cut(hole)
