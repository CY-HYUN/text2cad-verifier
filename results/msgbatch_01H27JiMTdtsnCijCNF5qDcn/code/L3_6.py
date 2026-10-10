import cadquery as cq
import math

R = 20.0
L = 100.0
amp = 30.0

# Base cylinder (built along Z, symmetric), then rotated so its axis is along Y (Front plane normal)
cyl = cq.Workplane("XY").circle(R).extrude(L / 2.0, both=True)

# Helical sine path: one full period around the circumference
n = 90
pts = []
for i in range(n):
    th = 2 * math.pi * i / n
    pts.append((R * math.cos(th), R * math.sin(th), amp * math.sin(th)))

path = cq.Workplane("XY").spline(pts, periodic=True)

# Profile plane at start point, normal to path tangent
tangent = cq.Vector(0, R, amp)  # d/dθ at θ=0
plane = cq.Plane(origin=(R, 0, 0), xDir=(1, 0, 0), normal=tangent.normalized().toTuple())

# Rectangle: 6 wide, radial extent 16..22 (4 mm deep below surface, with overshoot outside)
profile = cq.Workplane(plane).center(-3, 0).rect(6, 6)

groove = profile.sweep(path, isFrenet=True)

cam = cyl.cut(groove)

# Orient axis along Y
result = cam.rotate((0, 0, 0), (1, 0, 0), -90)
