import cadquery as cq
import math

R = 25.0
H = 100.0
depth = 5.0
half_w = 4.0

# base cylinder
base = cq.Workplane("XY").circle(R).extrude(H)

# sine groove: Y = 15*sin(k*X)+50, X = arc length along circumference (one period)
k = 2 * math.pi / (math.pi * 2 * R)

r_in = R - depth
r_out = R + 1.0
N = 72
wires = []
for i in range(N + 1):
    th = 2 * math.pi * i / N
    x = R * th
    zc = 15.0 * math.sin(k * x) + 50.0
    c, s = math.cos(th), math.sin(th)
    pts = [
        cq.Vector(r_in * c, r_in * s, zc - half_w),
        cq.Vector(r_out * c, r_out * s, zc - half_w),
        cq.Vector(r_out * c, r_out * s, zc + half_w),
        cq.Vector(r_in * c, r_in * s, zc + half_w),
    ]
    wires.append(cq.Wire.makePolygon(pts, close=True))

groove = cq.Solid.makeLoft(wires, False)

result = base.cut(cq.Workplane("XY").add(groove))
