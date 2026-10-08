import cadquery as cq
import math

# Hub
hub_d = 30.0
hub_h = 20.0
hub = cq.Workplane("XY").circle(hub_d / 2).extrude(hub_h)
zc = hub_h / 2

def bez(p0, p1, p2, p3, t):
    mt = 1 - t
    x = mt**3*p0[0] + 3*mt**2*t*p1[0] + 3*mt*t**2*p2[0] + t**3*p3[0]
    y = mt**3*p0[1] + 3*mt**2*t*p1[1] + 3*mt*t**2*p2[1] + t**3*p3[1]
    return (x, y)

# Normalized asymmetric teardrop airfoil (closed loop, no duplicate points)
N = 16
pts2d = []
up = [(1, 0), (0.6, 0.13), (0.0, 0.13), (0, 0)]
lo = [(0, 0), (0, -0.06), (0.5, -0.05), (1, 0)]
for i in range(N):
    pts2d.append(bez(*up, i / N))
for i in range(N):
    pts2d.append(bez(*lo, i / N))

def section(x, chord, ang_deg):
    a = math.radians(ang_deg)
    ca, sa = math.cos(a), math.sin(a)
    vecs = []
    for (u, v) in pts2d:
        uu = (u - 0.3) * chord
        vv = v * chord
        y = uu * ca - vv * sa
        z = zc + uu * sa + vv * ca
        vecs.append(cq.Vector(x, y, z))
    e = cq.Edge.makeSpline(vecs, periodic=True)
    return cq.Wire.assembleEdges([e])

r_root = hub_d / 2
L = 60.0
wires = [section(r_root - 4.0, 25.0, 45.0)]  # embedded in hub for clean union
n = 6
for i in range(n + 1):
    t = i / n
    x = r_root + t * L
    chord = 25.0 + (15.0 - 25.0) * t
    ang = 45.0 + (15.0 - 45.0) * t
    wires.append(section(x, chord, ang))

blade = cq.Solid.makeLoft(wires, False)

result = hub.union(cq.Workplane("XY").add(blade))
