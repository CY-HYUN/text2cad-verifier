import cadquery as cq
import math

# Gear parameters
m = 3.0
z = 20
alpha = math.radians(20)
width = 30.0

rp = m * z / 2.0              # 30
rb = rp * math.cos(alpha)     # base radius
ra = 33.0                     # tip radius
rf = 26.25                    # root radius

def inv(a):
    return math.tan(a) - a

def half_angle(r):
    if r <= rb:
        a_r = 0.0
    else:
        a_r = math.acos(rb / r)
    return math.pi / (2 * z) + inv(alpha) - inv(a_r)

def pol(r, t):
    return (r * math.cos(t), r * math.sin(t))

n_inv = 15
radii = [rb + (ra - rb) * i / n_inv for i in range(n_inv + 1)]
psi_b = half_angle(rb)
pitch_ang = 2 * math.pi / z

pts = []
for i in range(z):
    th = i * pitch_ang
    # right flank (lower angle side)
    pts.append(pol(rf, th - psi_b))
    for r in radii:
        pts.append(pol(r, th - half_angle(r)))
    # tip arc
    psi_a = half_angle(ra)
    for k in range(1, 4):
        t = -psi_a + 2 * psi_a * k / 4
        pts.append(pol(ra, th + t))
    # left flank
    for r in reversed(radii):
        pts.append(pol(r, th + half_angle(r)))
    pts.append(pol(rf, th + psi_b))
    # root arc midpoint to next tooth
    pts.append(pol(rf, th + pitch_ang / 2))

gear = cq.Workplane("XY").polyline(pts).close().extrude(width)

# Weight-reducing grooves on both faces (annulus 32-45 dia)
g_depth = 5.0
groove = (cq.Workplane("XY").circle(22.5).circle(16.0).extrude(g_depth))
gear = gear.cut(groove)
gear = gear.cut(groove.translate((0, 0, width - g_depth)))

# Shaft hole and keyway
hole = cq.Workplane("XY").circle(10.0).extrude(width)
key = cq.Workplane("XY").center(6.5, 0).rect(13.0, 6.0).extrude(width)
gear = gear.cut(hole.union(key))

result = gear
