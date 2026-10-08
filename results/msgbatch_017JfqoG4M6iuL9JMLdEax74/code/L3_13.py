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
    r = max(r, rb)
    ar = math.acos(rb / r)
    return math.pi / (2 * z) + inv(alpha) - inv(ar)

# Build closed outline
pts = []
n_flank = 12
radii = [rf] + [rb + (ra - rb) * i / n_flank for i in range(n_flank + 1)]
pitch_ang = 2 * math.pi / z
for i in range(z):
    th = i * pitch_ang
    # right flank (outward)
    for r in radii:
        a = th - half_angle(r)
        pts.append((r * math.cos(a), r * math.sin(a)))
    # tip arc
    psi_t = half_angle(ra)
    for k in range(1, 4):
        a = th - psi_t + 2 * psi_t * k / 4
        pts.append((ra * math.cos(a), ra * math.sin(a)))
    # left flank (inward)
    for r in reversed(radii):
        a = th + half_angle(r)
        pts.append((r * math.cos(a), r * math.sin(a)))
    # root arc to next tooth
    a0 = th + half_angle(rf)
    a1 = th + pitch_ang - half_angle(rf)
    for k in range(1, 4):
        a = a0 + (a1 - a0) * k / 4
        pts.append((rf * math.cos(a), rf * math.sin(a)))

gear = cq.Workplane("XY").polyline(pts).close().extrude(width)

# Shaft bore and keyway
bore = cq.Workplane("XY").circle(10.0).extrude(width)
key = cq.Workplane("XY").center(6.5, 0).rect(13.0, 6.0).extrude(width)
gear = gear.cut(bore.union(key))

# Weight-reducing annular grooves on both faces
depth = 4.0
groove_top = (cq.Workplane("XY").workplane(offset=width - depth)
              .circle(22.5).circle(16.0).extrude(depth))
groove_bot = (cq.Workplane("XY")
              .circle(22.5).circle(16.0).extrude(depth))
gear = gear.cut(groove_top).cut(groove_bot)

result = gear
