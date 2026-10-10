import cadquery as cq
import math

R_hub = 15.0
H_hub = 20.0
L = 60.0

def airfoil_pts(c, ang_deg, x):
    a = math.radians(ang_deg)
    n = 14
    ss = [0.5 * (1 - math.cos(math.pi * i / n)) for i in range(n + 1)]
    def thick(s):
        return 0.12 / 0.2 * (0.2969 * math.sqrt(s) - 0.1260 * s - 0.3516 * s**2
                             + 0.2843 * s**3 - 0.1036 * s**4)
    def camber(s):
        return 0.05 * 4 * s * (1 - s)
    up, lo = [], []
    for s in ss:
        yc = camber(s)
        yt = thick(s)
        for lst, sign in ((up, 1), (lo, -1)):
            u = (s - 0.5) * c
            v = (yc + sign * yt) * c
            Y = u * math.cos(a) - v * math.sin(a)
            Z = u * math.sin(a) + v * math.cos(a)
            lst.append(cq.Vector(x, Y, Z))
    return up, lo

def section(t):
    x = R_hub + L * t
    ang = 45 + (15 - 45) * t
    c = 25 + (15 - 25) * t
    up, lo = airfoil_pts(c, ang, x)
    lo[0] = up[0]
    lo[-1] = up[-1]
    e1 = cq.Edge.makeSpline(up)
    e2 = cq.Edge.makeSpline(lo[::-1])
    return cq.Wire.assembleEdges([e1, e2])

ts = [-0.05, 0.0, 0.25, 0.5, 0.75, 1.0]
wires = [section(t) for t in ts]
blade = cq.Solid.makeLoft(wires, False)

hub = cq.Workplane("XY").circle(R_hub).extrude(H_hub).translate((0, 0, -H_hub / 2))
result = hub.union(cq.Workplane("XY").add(blade))
