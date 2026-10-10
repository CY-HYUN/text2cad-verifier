import cadquery as cq
import math

# Hub: 30 mm dia, 20 mm tall, axis along Z
hub = cq.Workplane("XY").circle(15).extrude(20)

def airfoil_pts(chord, angle_deg, z0, n=12, t=0.12):
    a = math.radians(angle_deg)
    xs = [(1 - math.cos(math.pi * i / n)) / 2 for i in range(n + 1)]
    up, lo = [], []
    for x in xs:
        yt = 5 * t * (0.2969 * math.sqrt(x) - 0.1260 * x - 0.3516 * x**2
                      + 0.2843 * x**3 - 0.1036 * x**4)
        for lst, s in ((up, 1), (lo, -1)):
            u = x * chord
            v = s * yt * chord
            # rotate about the leading edge (origin), then place the LE at z0
            lst.append((u * math.cos(a) - v * math.sin(a),
                        u * math.sin(a) + v * math.cos(a) + z0))
    lower = lo[::-1]  # TE -> LE
    return up, lower

def draw(wp, chord, ang, z0):
    up, lower = airfoil_pts(chord, ang, z0)
    w = wp.moveTo(*up[0]).spline(up[1:], includeCurrent=True)
    w = w.lineTo(*lower[0]).spline(lower[1:], includeCurrent=True).close()
    return w

z0 = 2.0
ang_root, ang_tip = 45, 15

# Root stub embedded in hub so the blade has a proper connection
stub = draw(cq.Workplane("YZ", origin=(9, 0, 0)), 25, ang_root, z0).extrude(6)

# Loft from root plane (x=15) to tip plane (x=75)
wp = cq.Workplane("YZ", origin=(15, 0, 0))
wp = draw(wp, 25, ang_root, z0)
wp = wp.workplane(offset=60)
wp = draw(wp, 15, ang_tip, z0)
blade = wp.loft(ruled=False)

body = hub.union(stub).union(blade)

# Fillet at blade/hub junction: edges lying on the hub cylinder surface
def on_junction(e):
    pts = [e.positionAt(p) for p in (0.0, 0.25, 0.5, 0.75, 1.0)]
    for p in pts:
        if abs(math.hypot(p.x, p.y) - 15) > 0.05:
            return False
        if p.z < 0.3 or p.z > 19.7:
            return False
    return True

try:
    edges = [e for e in body.edges().vals() if e.geomType() != "LINE" and on_junction(e)]
    if edges:
        result = body.newObject(edges).fillet(2.0)
    else:
        result = body
except Exception:
    result = body
