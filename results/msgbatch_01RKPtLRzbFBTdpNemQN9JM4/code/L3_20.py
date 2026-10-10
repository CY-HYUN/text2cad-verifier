import cadquery as cq
import math

# Hub: diameter 30, height 20, axis along Z
hub = cq.Workplane("XY").circle(15).extrude(20).translate((0, 0, -10))

# Airfoil profile (asymmetric teardrop), normalized chord 0..1
N = 12
def profile():
    ups, los = [], []
    for i in range(N + 1):
        b = i / N
        s = 0.5 * (1 - math.cos(math.pi * b))  # cosine spacing
        yt = 0.6 * 0.12 * (0.2969 * math.sqrt(s) - 0.1260 * s - 0.3516 * s**2
                           + 0.2843 * s**3 - 0.1036 * s**4)
        yc = 0.05 * math.sin(math.pi * s) * (1 - 0.3 * s)
        ups.append((s, yc + yt))
        los.append((s, yc - yt))
    return ups, los

UP, LO = profile()

def section(x, chord, ang_deg):
    a = math.radians(ang_deg)
    ca, sa = math.cos(a), math.sin(a)
    def tr(p):
        u = (p[0] - 0.5) * chord
        v = p[1] * chord
        return cq.Vector(x, u * ca - v * sa, u * sa + v * ca)
    up = [tr(p) for p in UP]
    lo = [tr(p) for p in LO]
    lo[0] = up[0]
    lo[-1] = up[-1]
    e1 = cq.Edge.makeSpline(up)
    e2 = cq.Edge.makeSpline(lo)
    return cq.Wire.assembleEdges([e1, e2])

# Root stub embedded in hub (same root section)
w0 = section(8, 25, 45)
w1 = section(15, 25, 45)
stub = cq.Solid.makeLoft([w0, w1], True)

# Main blade: x=15 (root) to x=75 (tip), twist 45 -> 15 deg, chord 25 -> 15
wr = section(15, 25, 45)
wm = section(45, 20, 30)
wt = section(75, 15, 15)
blade = cq.Solid.makeLoft([wr, wm, wt], False)

result = hub.union(cq.Workplane("XY").add(stub)).union(cq.Workplane("XY").add(blade))
