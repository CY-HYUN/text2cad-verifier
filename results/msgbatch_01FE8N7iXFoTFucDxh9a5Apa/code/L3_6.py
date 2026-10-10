import cadquery as cq
import math

R = 20.0
L = 100.0
A = 30.0
zc = L / 2.0
groove_r = 3.0

body = cq.Workplane("XY").circle(R).extrude(L)

def make_tube(rc):
    n = 96
    pts = []
    for i in range(n):
        phi = 2 * math.pi * i / n
        pts.append((rc * math.cos(phi), rc * math.sin(phi), zc + A * math.sin(phi)))
    path = cq.Workplane("XY").spline(pts, periodic=True)
    p0 = cq.Vector(rc, 0, zc)
    tangent = cq.Vector(0, rc, A).normalized()
    plane = cq.Plane(origin=p0, xDir=cq.Vector(1, 0, 0), normal=tangent)
    tube = cq.Workplane(plane).circle(groove_r).sweep(path, transition="round")
    return tube

result = body
# Bottom at r = 16 (depth 4); stacked tubes form a U-shape with ~6 mm width at surface
for rc in [19.0, 20.0, 21.0, 22.0]:
    try:
        result = result.cut(make_tube(rc))
    except Exception:
        pass
