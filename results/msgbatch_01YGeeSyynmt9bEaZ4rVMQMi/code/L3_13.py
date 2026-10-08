import cadquery as cq
import math

# Parameters
m = 3.0
z = 20
alpha = math.radians(20.0)
d = m * z                      # 60 pitch diameter
db = d * math.cos(alpha)       # base circle diameter
ra = 66.0 / 2.0                # tip radius
rr = 52.5 / 2.0                # root radius
rb = db / 2.0
width = 30.0

def inv(a):
    return math.tan(a) - a

# half tooth angle at base circle
theta_b = math.pi / (2 * z) + inv(alpha)

def theta(r):
    if r <= rb:
        return theta_b
    a = math.acos(rb / r)
    return theta_b - inv(a)

def pol(r, ang):
    return (r * math.cos(ang), r * math.sin(ang))

n_flank = 15
n_tip = 4
n_root = 6
rs = [rb + (ra - rb) * i / n_flank for i in range(n_flank + 1)]

pts = []
pitch_ang = 2 * math.pi / z
for i in range(z):
    c = i * pitch_ang
    # root point before tooth
    pts.append(pol(rr, c - theta_b))
    # lower flank (involute) going up
    for r in rs:
        pts.append(pol(r, c - theta(r)))
    # tip arc interior
    ta = theta(ra)
    for k in range(1, n_tip):
        ang = c - ta + 2 * ta * k / n_tip
        pts.append(pol(ra, ang))
    # upper flank (mirrored involute) going down
    for r in reversed(rs):
        pts.append(pol(r, c + theta(r)))
    # root point after tooth
    pts.append(pol(rr, c + theta_b))
    # root arc interior
    a0 = c + theta_b
    a1 = c + pitch_ang - theta_b
    for k in range(1, n_root):
        pts.append(pol(rr, a0 + (a1 - a0) * k / n_root))

gear = cq.Workplane("XY").polyline(pts).close().extrude(width)

# Grooves on both end faces: dia 45, depth 3
groove_top = cq.Workplane("XY").workplane(offset=width - 3.0).circle(22.5).extrude(3.0)
groove_bot = cq.Workplane("XY").circle(22.5).extrude(3.0)
gear = gear.cut(groove_top).cut(groove_bot)

# Center bore dia 20 with 6x3 keyway
bore = cq.Workplane("XY").circle(10.0).extrude(width)
key = (cq.Workplane("XY")
       .center(0, (10.0 + 3.0) / 2.0)
       .rect(6.0, 13.0)
       .extrude(width))
gear = gear.cut(bore.union(key))

result = gear
