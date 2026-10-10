import cadquery as cq
import math

m = 3.0
z = 20
alpha = math.radians(20)
W = 15.0
rp = m * z / 2
ra = rp + m
rf = rp - 1.25 * m
rb = rp * math.cos(alpha)

def inv(a):
    return math.tan(a) - a

def theta(r):
    # half angular thickness of tooth at radius r
    a = math.acos(min(1.0, rb / r))
    return math.pi / (2 * z) + inv(alpha) - inv(a)

def pol(r, ang):
    return (r * math.cos(ang), r * math.sin(ang))

n = 8
rs = [rb + (ra - rb) * i / n for i in range(n + 1)]
thb = theta(rb)
tha = theta(ra)

start = pol(rf, -thb)
w = cq.Workplane("XY").moveTo(*start)
for i in range(z):
    phi = i * 2 * math.pi / z
    w = w.lineTo(*pol(rb, phi - thb))
    pts = [pol(r, phi - theta(r)) for r in rs[1:]]
    w = w.spline(pts, includeCurrent=True)
    w = w.threePointArc(pol(ra, phi), pol(ra, phi + tha))
    pts = [pol(r, phi + theta(r)) for r in reversed(rs[:-1])]
    w = w.spline(pts, includeCurrent=True)
    w = w.lineTo(*pol(rf, phi + thb))
    phin = (i + 1) * 2 * math.pi / z
    w = w.threePointArc(pol(rf, phi + math.pi / z), pol(rf, phin - thb))
w = w.close()
gear = w.extrude(W)

# root fillet
try:
    edges = [e for e in gear.edges("|Z").vals()
             if abs(math.hypot(e.Center().x, e.Center().y) - rf) < 0.01]
    gear = gear.newObject(edges).fillet(0.9)
except Exception:
    pass

# bore and keyway
bore = cq.Workplane("XY").circle(10.0).extrude(W)
key = (cq.Workplane("XY").center(6.5, 0).rect(13.0, 6.0).extrude(W)
       .rotate((0, 0, 0), (0, 0, 1), math.degrees(math.pi / z)))
result = gear.cut(bore).cut(key)
