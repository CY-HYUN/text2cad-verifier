import cadquery as cq
import math

N = 400
T = 10 * math.pi
w, t = 8.0, 1.2

def f(th):
    # linear decay factor over the last pi/2 at each end
    return max(0.0, min(1.0, th / (math.pi / 2), (T - th) / (math.pi / 2)))

ths = [T * i / N for i in range(N + 1)]
# base rise with pitch tapering to 0 at the ends (numerical integration)
zbase = [0.0]
for i in range(1, N + 1):
    a, b = ths[i - 1], ths[i]
    rate = lambda th: 8.0 / (2 * math.pi) * f(th)
    zbase.append(zbase[-1] + 0.5 * (rate(a) + rate(b)) * (b - a))

wires = []
for th, zb in zip(ths, zbase):
    R = 40 - 1.5 * th / (2 * math.pi)
    z = zb + 2.5 * math.sin(6 * th) * f(th)
    c, s = math.cos(th), math.sin(th)
    pts = []
    for dr, dz in [(-w / 2, -t / 2), (w / 2, -t / 2), (w / 2, t / 2), (-w / 2, t / 2)]:
        r = R + dr
        pts.append(cq.Vector(r * c, r * s, z + dz))
    wires.append(cq.Wire.makePolygon(pts, close=True))

solid = cq.Solid.makeLoft(wires, True)
result = cq.Workplane("XY").add(solid)
