import cadquery as cq
import math

# Parameters
m = 3.0
z = 20
alpha = math.radians(20.0)
d = m * z                 # 60
db = d * math.cos(alpha)  # base circle diameter
rb = db / 2.0
ra = 66.0 / 2.0           # tip radius
rf = 52.5 / 2.0           # root radius
width = 30.0

def inv(a):
    return math.tan(a) - a

# angular offset of involute start (base circle) from tooth centerline
beta0 = math.pi / (2 * z) + inv(alpha)

def flank_angle(r):
    r = max(r, rb)
    a = math.acos(rb / r)
    return beta0 - inv(a)

n_flank = 15
radii = [rb + (ra - rb) * i / n_flank for i in range(n_flank + 1)]

pts = []
pitch_ang = 2 * math.pi / z
for i in range(z):
    c = i * pitch_ang
    # lower flank: root -> base -> tip
    pts.append((rf * math.cos(c - beta0), rf * math.sin(c - beta0)))
    for r in radii:
        th = c - flank_angle(r)
        pts.append((r * math.cos(th), r * math.sin(th)))
    # tip arc
    t0 = c - flank_angle(ra)
    t1 = c + flank_angle(ra)
    for k in range(1, 4):
        th = t0 + (t1 - t0) * k / 4
        pts.append((ra * math.cos(th), ra * math.sin(th)))
    # upper flank: tip -> base
    for r in reversed(radii):
        th = c + flank_angle(r)
        pts.append((r * math.cos(th), r * math.sin(th)))
    pts.append((rf * math.cos(c + beta0), rf * math.sin(c + beta0)))
    # root arc to next tooth
    s0 = c + beta0
    s1 = c + pitch_ang - beta0
    for k in range(1, 5):
        th = s0 + (s1 - s0) * k / 5
        pts.append((rf * math.cos(th), rf * math.sin(th)))

gear = cq.Workplane("XY").polyline(pts).close().extrude(width)

# Grooves on both end faces (dia 45, depth 3)
groove_top = cq.Workplane("XY").workplane(offset=width - 3.0).circle(22.5).extrude(3.0)
groove_bot = cq.Workplane("XY").circle(22.5).extrude(3.0)
gear = gear.cut(groove_top).cut(groove_bot)

# Bore dia 20 with 6x3 keyway
bore = cq.Workplane("XY").circle(10.0).extrude(width)
key = cq.Workplane("XY").center(6.5, 0).rect(13.0, 6.0).extrude(width)
gear = gear.cut(bore).cut(key)

result = gear
