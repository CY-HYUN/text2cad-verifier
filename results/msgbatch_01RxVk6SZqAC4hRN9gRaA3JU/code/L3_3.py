import cadquery as cq
import math

# Parameters
m = 3.0
z = 20
alpha = math.radians(20.0)
D = m * z                      # 60
rp = D / 2.0                   # 30
rb = rp * math.cos(alpha)      # 28.19
ra = rp + m                    # 33
rf = rp - 1.25 * m             # 26.25
thk = 15.0

def inv(a):
    return math.tan(a) - a

# tooth half-thickness angle at pitch circle (s = pi*m/2)
half_pitch_ang = (math.pi * m / 2.0) / (2.0 * rp)
theta0 = half_pitch_ang + inv(alpha)   # half angle at base circle

def pol(r, a):
    return (r * math.cos(a), r * math.sin(a))

N = 12
radii = [rb + (ra - rb) * i / N for i in range(N + 1)]
pitch = 2 * math.pi / z

start = pol(rf, -theta0)
wp = cq.Workplane("XY").moveTo(*start)

for i in range(z):
    phi = i * pitch
    # side A (lower angle), going up
    wp = wp.lineTo(*pol(rb, phi - theta0))
    for r in radii[1:]:
        a = math.acos(rb / r)
        wp = wp.lineTo(*pol(r, phi - (theta0 - inv(a))))
    # tip arc
    at = math.acos(rb / ra)
    wp = wp.threePointArc(pol(ra, phi), pol(ra, phi + (theta0 - inv(at))))
    # side B, going down
    for r in reversed(radii[:-1]):
        a = math.acos(rb / r)
        wp = wp.lineTo(*pol(r, phi + (theta0 - inv(a))))
    wp = wp.lineTo(*pol(rf, phi + theta0))
    # root arc to next tooth
    nphi = phi + pitch
    wp = wp.threePointArc(pol(rf, phi + pitch / 2.0), pol(rf, nphi - theta0))

gear = wp.close().extrude(thk)

# Root fillets 0.9 mm
try:
    solid = gear.val()
    root_edges = []
    for e in solid.Edges():
        if e.geomType() != "LINE":
            continue
        bb = e.BoundingBox()
        if bb.zlen < thk - 1e-3:
            continue
        c = e.Center()
        if abs(math.hypot(c.x, c.y) - rf) < 1e-3:
            root_edges.append(e)
    if root_edges:
        gear = cq.Workplane("XY").add(solid.fillet(0.9, root_edges))
except Exception:
    pass

# Bore with keyway, cut through all
bore = cq.Workplane("XY").circle(10.0).extrude(thk)
key = cq.Workplane("XY").center(6.5, 0).rect(13.0, 6.0).extrude(thk)
cutter = bore.union(key)

result = gear.cut(cutter)
