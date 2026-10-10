import cadquery as cq
import math

base_r = 60.0
base_t = 10.0
wall_h = 25.0
wall_t = 4.0
half = wall_t / 2.0

# base disc with central exhaust hole
base = cq.Workplane("XY").circle(base_r).extrude(base_t)
base = base.cut(cq.Workplane("XY").circle(4.0).extrude(base_t))

# spiral centerline r = 20 + 3.5*theta, theta 0..3pi
N = 160
th_end = 3 * math.pi
left = []
right = []
for i in range(N + 1):
    t = th_end * i / N
    r = 20 + 3.5 * t
    x = r * math.cos(t)
    y = r * math.sin(t)
    dx = 3.5 * math.cos(t) - r * math.sin(t)
    dy = 3.5 * math.sin(t) + r * math.cos(t)
    l = math.hypot(dx, dy)
    nx, ny = dy / l, -dx / l
    left.append((x + nx * half, y + ny * half))
    right.append((x - nx * half, y - ny * half))

pts = left + right[::-1]
wall = (cq.Workplane("XY").workplane(offset=base_t)
        .polyline(pts).close().extrude(wall_h))

# rounded (R2) ends of the wall
def end_cap(t):
    r = 20 + 3.5 * t
    return (cq.Workplane("XY").workplane(offset=base_t)
            .center(r * math.cos(t), r * math.sin(t))
            .circle(half).extrude(wall_h))

wall = wall.union(end_cap(0.0)).union(end_cap(th_end))

result = base.union(wall)
