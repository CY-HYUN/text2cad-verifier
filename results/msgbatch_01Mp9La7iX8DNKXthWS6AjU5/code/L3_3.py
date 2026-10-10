import cadquery as cq
import math

m = 3.0
z = 20
alpha = math.radians(20)
D = m * z
rp = D / 2
rb = rp * math.cos(alpha)      # 28.19
rt = rp + m                    # tip radius
rf = rp - 1.25 * m             # root radius
T = 15.0

def inv(t):
    return t - math.atan(t)

tp = math.tan(alpha)
inv_p = inv(tp)
half = math.pi / (2 * z)       # half tooth angle at pitch circle (thickness = pi*m/2)
t_tip = math.sqrt((rt / rb) ** 2 - 1)

def pol(r, a):
    return (r * math.cos(a), r * math.sin(a))

def flank_pts(n=12):
    pts = []
    for i in range(n + 1):
        t = t_tip * i / n
        r = rb * math.sqrt(1 + t * t)
        a = half - (inv(t) - inv_p)   # upper flank angle (tooth centred on angle 0)
        pts.append((r, a))
    return pts

fl = flank_pts()
pitch = 2 * math.pi / z
a0 = fl[0][1]   # base angle of upper flank

w = cq.Workplane("XY")
start = pol(rf, -a0)
w = w.moveTo(*start)
for i in range(z):
    c = i * pitch
    # lower flank (mirrored)
    w = w.lineTo(*pol(rb, c - a0))
    low = [pol(r, c - a) for r, a in fl[1:]]
    w = w.spline(low, includeCurrent=True)
    # tip arc
    a_tip = fl[-1][1]
    w = w.threePointArc(pol(rt, c), pol(rt, c + a_tip))
    # upper flank down
    up = [pol(r, c + a) for r, a in reversed(fl[:-1])]
    w = w.spline(up, includeCurrent=True)
    w = w.lineTo(*pol(rf, c + a0))
    # root arc to next tooth
    nc = c + pitch
    mid = (c + a0 + nc - a0) / 2
    if i < z - 1:
        w = w.threePointArc(pol(rf, mid), pol(rf, nc - a0))
    else:
        w = w.threePointArc(pol(rf, mid), start)
w = w.close()
gear = w.extrude(T)

# root fillet 0.9
try:
    sel = [e for e in gear.val().Edges()
           if abs(e.Center().z - T / 2) < 1e-3
           and abs(math.hypot(e.Center().x, e.Center().y) - rf) < 0.05
           and abs(e.Length() - T) < 1e-3]
    filleted = gear.val().fillet(0.9, sel)
    gear = cq.Workplane("XY").add(filleted)
except Exception:
    pass

# bore 20 mm and keyway 6 x 3 mm
bore = cq.Workplane("XY").circle(10.0).extrude(T)
key = cq.Workplane("XY").center(0, 10 + 1.5 - 0.0).rect(6, 6).extrude(T)
key = cq.Workplane("XY").moveTo(-3, 0).lineTo(3, 0).lineTo(3, 13).lineTo(-3, 13).close().extrude(T)
result = gear.cut(bore).cut(key)
