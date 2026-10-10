import cadquery as cq
import math

m = 3.0
z = 20
alpha = math.radians(20)
width = 15.0
rp = m * z / 2.0              # 30
ra = rp + m                   # 33
rf = rp - 1.25 * m            # 26.25
rb = rp * math.cos(alpha)
rho = 0.9

def inv(a):
    return math.tan(a) - a

beta_b = math.pi / (2 * z) + inv(alpha)

def half_angle(r):
    a = math.acos(min(1.0, rb / r))
    return beta_b - inv(a)

def pol(r, t):
    return (r * math.cos(t), r * math.sin(t))

# fillet geometry
rc = rf + rho
delta = math.asin(rho / rc)

def fillet_pts(theta_line, sign):
    # sign=-1: fillet on lower-angle side of line; +1 on higher side
    tc = theta_line + sign * delta
    C = pol(rc, tc)
    P1 = pol(rf, tc)
    P2 = pol(rc * math.cos(delta), theta_line)
    a1 = math.atan2(P1[1] - C[1], P1[0] - C[0])
    a2 = math.atan2(P2[1] - C[1], P2[0] - C[0])
    d = a2 - a1
    while d > math.pi:
        d -= 2 * math.pi
    while d < -math.pi:
        d += 2 * math.pi
    n = 6
    return [(C[0] + rho * math.cos(a1 + d * i / n),
             C[1] + rho * math.sin(a1 + d * i / n)) for i in range(n + 1)]

pts = []
pitch = 2 * math.pi / z
nflank = 15
radii = [rb + (ra - rb) * (i / nflank) ** 1.5 for i in range(nflank + 1)]

for k in range(z):
    c = (k + 0.5) * pitch   # tooth spaces centered at angle 0 (keyway direction)
    # right flank (lower angle side)
    th = c - beta_b
    pts += fillet_pts(th, -1)
    for r in radii:
        pts.append(pol(r, c - half_angle(r)))
    # tip arc
    ht = half_angle(ra)
    for i in range(1, 4):
        pts.append(pol(ra, c - ht + 2 * ht * i / 4))
    # left flank down
    for r in reversed(radii):
        pts.append(pol(r, c + half_angle(r)))
    fp = fillet_pts(c + beta_b, +1)
    pts += list(reversed(fp))
    # root arc to next tooth
    t0 = c + beta_b + delta
    t1 = c + pitch - beta_b - delta
    for i in range(1, 4):
        pts.append(pol(rf, t0 + (t1 - t0) * i / 4))

# remove near-duplicates
clean = []
for p in pts:
    if not clean or math.hypot(p[0] - clean[-1][0], p[1] - clean[-1][1]) > 1e-4:
        clean.append(p)
if math.hypot(clean[0][0] - clean[-1][0], clean[0][1] - clean[-1][1]) < 1e-4:
    clean.pop()

gear = cq.Workplane("XY").polyline(clean).close().extrude(width)

# shaft hole
hole = cq.Workplane("XY").circle(10.0).extrude(width)
gear = gear.cut(hole)

# keyway along +X (aligned with tooth space centered at angle 0)
key = cq.Workplane("XY").center(13.0 / 2.0, 0).rect(13.0, 6.0).extrude(width)
gear = gear.cut(key)

result = gear
