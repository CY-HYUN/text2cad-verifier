import cadquery as cq
import math

# Parameters
base_d = 120.0
base_t = 10.0
wall_h = 25.0
wall_t = 4.0
r0 = 20.0
k = 3.5
th_end = 3 * math.pi
hole_d = 8.0
n = 300

# Base disc
base = cq.Workplane("XY").circle(base_d / 2).extrude(base_t)

# Spiral wall profile (offset +/- half thickness about centerline)
half = wall_t / 2
outer = []
inner = []
for i in range(n + 1):
    th = th_end * i / n
    r = r0 + k * th
    outer.append(((r + half) * math.cos(th), (r + half) * math.sin(th)))
    inner.append(((r - half) * math.cos(th), (r - half) * math.sin(th)))
pts = outer + inner[::-1]

wall = (
    cq.Workplane("XY")
    .workplane(offset=base_t)
    .polyline(pts)
    .close()
    .extrude(wall_h)
)

# Rounded ends (R2) at both ends of the wall
for th in (0.0, th_end):
    r = r0 + k * th
    cap = (
        cq.Workplane("XY")
        .workplane(offset=base_t)
        .center(r * math.cos(th), r * math.sin(th))
        .circle(half)
        .extrude(wall_h)
    )
    wall = wall.union(cap)

result = base.union(wall)

# Central exhaust hole
hole = cq.Workplane("XY").workplane(offset=-1).circle(hole_d / 2).extrude(base_t + 2)
result = result.cut(hole)
