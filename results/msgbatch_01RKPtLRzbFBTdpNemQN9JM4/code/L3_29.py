import cadquery as cq
import math

turns = 5
per_turn = 72
N = turns * per_turn
theta_end = 2 * math.pi * turns
ramp = math.pi / 2
width = 8.0
thick = 1.2

def decay(t):
    return max(0.0, min(1.0, t / ramp, (theta_end - t) / ramp))

# sample angles
thetas = [theta_end * i / N for i in range(N + 1)]

# base rise integrated with pitch flattening at both ends (numerical integration)
zbase = [0.0]
for i in range(1, N + 1):
    t0, t1 = thetas[i - 1], thetas[i]
    tm = 0.5 * (t0 + t1)
    dz = 8.0 / (2 * math.pi) * decay(tm) * (t1 - t0)
    zbase.append(zbase[-1] + dz)

wires = []
for i, t in enumerate(thetas):
    R = 40.0 - 1.5 * (t / (2 * math.pi))
    z = zbase[i] + 2.5 * decay(t) * math.sin(6 * t)
    er = (math.cos(t), math.sin(t))
    pts = []
    for dr, dz in [(-width / 2, -thick / 2), (width / 2, -thick / 2),
                   (width / 2, thick / 2), (-width / 2, thick / 2)]:
        rr = R + dr
        pts.append(cq.Vector(rr * er[0], rr * er[1], z + dz))
    pts.append(pts[0])
    wires.append(cq.Wire.makePolygon(pts))

solid = cq.Solid.makeLoft(wires, True)
result = cq.Workplane("XY").newObject([solid])
