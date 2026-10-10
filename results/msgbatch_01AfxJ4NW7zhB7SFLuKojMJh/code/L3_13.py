import cadquery as cq
import math

m = 3.0
z = 20
alpha = math.radians(20)
width = 30.0
rp = m * z / 2.0
rb = rp * math.cos(alpha)
ra = 33.0
rr = 26.25

def inv(a):
    return math.tan(a) - a

def half_angle(r):
    a = math.acos(min(1.0, rb / r))
    return math.pi / (2 * z) + inv(alpha) - inv(a)

pts = []
n = 8
for i in range(z):
    c = 2 * math.pi * i / z
    hb = half_angle(rb)
    # root point, right side
    pts.append((rr * math.cos(c - hb), rr * math.sin(c - hb)))
    rs = [rb + (ra - rb) * k / n for k in range(n + 1)]
    for r in rs:
        t = c - half_angle(r)
        pts.append((r * math.cos(t), r * math.sin(t)))
    for r in reversed(rs):
        t = c + half_angle(r)
        pts.append((r * math.cos(t), r * math.sin(t)))
    pts.append((rr * math.cos(c + hb), rr * math.sin(c + hb)))

gear = cq.Workplane("XY").polyline(pts).close().extrude(width)

# bore
gear = gear.cut(cq.Workplane("XY").circle(10).extrude(width))
# keyway
key = cq.Workplane("XY").center(0, 6.5).rect(6, 13).extrude(width)
gear = gear.cut(key.cut(cq.Workplane("XY").circle(5).extrude(width)).union(
    cq.Workplane("XY").center(0, 11.5).rect(6, 3).extrude(width)))
# weight-reducing grooves on both faces
depth = 5.0
ring = cq.Workplane("XY").circle(22.5).circle(16).extrude(depth)
gear = gear.cut(ring)
gear = gear.cut(ring.translate((0, 0, width - depth)))

result = gear
