import cadquery as cq
import math

# Parameters
m = 3.0
z = 20
alpha = math.radians(20.0)
thk = 15.0
D = m * z                      # 60
rp = D / 2.0                   # 30
rb = rp * math.cos(alpha)      # 28.19
ra = rp + m                    # 33
rf = rp - 1.25 * m             # 26.25

def inv(a):
    return math.tan(a) - a

# half tooth angle at base circle (tooth thickness pi*m/2 at pitch circle)
half_p = (math.pi * m / 2.0) / (2.0 * rp)
hb = half_p + inv(alpha)

def pol(r, ang):
    return (r * math.cos(ang), r * math.sin(ang))

def phi(r):
    a = math.acos(min(1.0, rb / r))
    return inv(a)

N = 12
radii = [rb + (ra - rb) * i / N for i in range(N + 1)]
pitch = 2 * math.pi / z

wp = cq.Workplane("XY")
start = pol(rf, -hb)
wp = wp.moveTo(*start)
for i in range(z):
    tc = i * pitch
    # radial line root -> base
    wp = wp.lineTo(*pol(rb, tc - hb))
    # right flank involute (equation curve, base radius 28.19)
    right = [pol(r, tc - hb + phi(r)) for r in radii[1:]]
    wp = wp.spline(right, includeCurrent=True)
    # tip arc
    tip_half = hb - phi(ra)
    wp = wp.threePointArc(pol(ra, tc), pol(ra, tc + tip_half))
    # left flank (mirror)
    left = [pol(r, tc + hb - phi(r)) for r in reversed(radii[:-1])]
    wp = wp.spline(left, includeCurrent=True)
    # radial line base -> root
    wp = wp.lineTo(*pol(rf, tc + hb))
    # root arc to next tooth
    nxt = (i + 1) * pitch
    if i < z - 1:
        wp = wp.threePointArc(pol(rf, tc + pitch / 2.0), pol(rf, nxt - hb))
    else:
        wp = wp.threePointArc(pol(rf, tc + pitch / 2.0), start)
gear = wp.close().extrude(thk)

# Root fillet 0.9 mm
try:
    solid = gear.val()
    edges = []
    for e in solid.Edges():
        p0 = e.startPoint()
        p1 = e.endPoint()
        if abs(p0.x - p1.x) < 1e-4 and abs(p0.y - p1.y) < 1e-4 and abs(p0.z - p1.z) > 1e-3:
            if abs(math.hypot(p0.x, p0.y) - rf) < 0.05:
                edges.append(e)
    if edges:
        gear = cq.Workplane("XY").add(solid.fillet(0.9, edges))
except Exception:
    pass

# Center bore D20 and keyway 6x3, cut through all
bore = cq.Workplane("XY").circle(10.0).extrude(thk)
key = cq.Workplane("XY").center(0, (10.0 + 3.0) / 2.0).rect(6.0, 10.0 + 3.0).extrude(thk)
result = gear.cut(bore).cut(key)
