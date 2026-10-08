import cadquery as cq
import math

T = 10 * math.pi          # 5 turns
L = math.pi / 2           # end transition range
p = 8.0 / (2 * math.pi)   # rise per radian (8 mm per turn)
A = 2.5                   # wave amplitude
W = 8.0                   # section width (radial, parallel to XY)
H = 1.2                   # section thickness (axial)

def g(t):
    # integrated pitch factor: pitch ramps linearly to 0 at both ends
    if t < L:
        return t * t / (2 * L)
    if t <= T - L:
        return L / 2 + (t - L)
    s = t - (T - L)
    return L / 2 + (T - 2 * L) + s - s * s / (2 * L)

def amp(t):
    return min(1.0, t / L, (T - t) / L)

def R(t):
    return 40.0 - 1.5 * (t / (2 * math.pi))

def Z(t):
    return p * g(t) + A * amp(t) * math.sin(6 * t)

N = 1200
corners = [(-W / 2, -H / 2), (W / 2, -H / 2), (W / 2, H / 2), (-W / 2, H / 2)]
pts = [[] for _ in corners]
for i in range(N + 1):
    t = T * i / N
    r = R(t)
    z = Z(t)
    c, s = math.cos(t), math.sin(t)
    for k, (dr, dz) in enumerate(corners):
        rr = r + dr
        pts[k].append(cq.Vector(rr * c, rr * s, z + dz))

edges = [cq.Edge.makeSpline(pl) for pl in pts]

faces = []
for k in range(4):
    faces.append(cq.Face.makeRuledSurface(edges[k], edges[(k + 1) % 4]))

# planar end caps (radial-axial plane, perpendicular to helix tangent in plan)
for idx in (0, N):
    w = cq.Wire.makePolygon([pts[k][idx] for k in range(4)] + [pts[0][idx]])
    faces.append(cq.Face.makeFromWires(w))

shell = cq.Shell.makeShell(faces)
solid = cq.Solid.makeSolid(shell)
try:
    solid = solid.fix()
except Exception:
    pass

result = cq.Workplane("XY").newObject([solid])
