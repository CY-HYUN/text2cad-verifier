import cadquery as cq
import math

# Datum heights
z1, z2, z3 = 0.0, 75.0, 150.0

# Wavy profile on Plane2: 6 periods, radius 30..40 (centre 35, amplitude 5)
n_per = 6
pts_per = 8
N = n_per * pts_per
pts = []
for i in range(N):
    t = 2 * math.pi * i / N
    r = 35.0 + 5.0 * math.sin(n_per * t)
    pts.append((r * math.cos(t), r * math.sin(t)))

wp = (
    cq.Workplane("XY").workplane(offset=z1).circle(30.0)          # bottom circle, dia 60
    .workplane(offset=z2 - z1)
    .spline(pts, periodic=True).close()                           # wavy middle ring
    .workplane(offset=z3 - z2).circle(40.0)                       # top circle, dia 80
    .loft(ruled=False, combine=True)
)

# Shell into a container: remove top face, 2 mm wall
result = wp.faces(">Z").shell(-2.0)
