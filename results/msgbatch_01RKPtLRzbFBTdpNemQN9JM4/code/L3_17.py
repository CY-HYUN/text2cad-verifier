import cadquery as cq
import math

R = 25.0
L = 100.0
amp = 15.0
zc = 50.0
rc = 24.0  # radius of the groove centerline (semicircle centre); bottom at r=20 -> depth 5

body = cq.Workplane("XY").circle(R).extrude(L)

n = 72
pts = []
for i in range(n):
    t = 2 * math.pi * i / n
    pts.append((rc * math.cos(t), rc * math.sin(t), zc + amp * math.sin(t)))

path = cq.Workplane("XY").spline(pts, periodic=True)

# tangent at t=0
tx = (0.0, rc, amp)
mag = math.sqrt(tx[1] ** 2 + tx[2] ** 2)
normal = (0.0, tx[1] / mag, tx[2] / mag)
plane = cq.Plane(origin=pts[0], xDir=(1, 0, 0), normal=normal)

# semicircular bottom
circ = cq.Workplane(plane).circle(4.0).sweep(path, isFrenet=True)
# straight walls from the semicircle centre out through the surface
rect = (cq.Workplane(plane).center(1.5, 0).rect(3.0, 8.0)
        .sweep(path, isFrenet=True))

result = body.cut(circ).cut(rect)
