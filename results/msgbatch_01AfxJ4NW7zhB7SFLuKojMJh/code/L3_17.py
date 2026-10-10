import cadquery as cq
import math

R = 25.0
L = 100.0
rc = 24.0  # groove centerline radius (semicircle centre); depth 5 mm at the bottom
A = 15.0
Z0 = 50.0
N = 72

body = cq.Workplane("XY").circle(R).extrude(L)

pts = []
for i in range(N + 1):
    t = 2 * math.pi * i / N
    pts.append((rc * math.cos(t), rc * math.sin(t), Z0 + A * math.sin(t)))

tan = (0.0, rc, A)
path = cq.Workplane("XY").spline(pts, tangents=[tan, tan], includeCurrent=False)

plane = cq.Plane(origin=pts[0], xDir=(1, 0, 0), normal=tan)

tube = (cq.Workplane(plane).circle(4.0).sweep(path, isFrenet=True))
slot = (cq.Workplane(plane).center(1.5, 0).rect(3.0, 8.0).sweep(path, isFrenet=True))

tool = tube.union(slot)
result = body.cut(tool)
