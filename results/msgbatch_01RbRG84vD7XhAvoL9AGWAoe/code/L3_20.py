import cadquery as cq
import math

# Hub
hub_d = 30.0
hub_h = 20.0
hub = cq.Workplane("XY").circle(hub_d / 2).extrude(hub_h).translate((0, 0, -hub_h / 2))

blade_len = 60.0
r_root = hub_d / 2
r_tip = r_root + blade_len
root_chord, tip_chord = 25.0, 15.0
root_ang, tip_ang = 45.0, 15.0


def bezier(p0, p1, p2, p3, n=24):
    pts = []
    for i in range(n + 1):
        t = i / n
        a = (1 - t) ** 3
        b = 3 * (1 - t) ** 2 * t
        c = 3 * (1 - t) * t ** 2
        d = t ** 3
        pts.append((a * p0[0] + b * p1[0] + c * p2[0] + d * p3[0],
                    a * p0[1] + b * p1[1] + c * p2[1] + d * p3[1]))
    return pts


def section(x, chord, ang_deg):
    c = chord
    upper = bezier((0, 0), (0, 0.16 * c), (0.45 * c, 0.12 * c), (c, 0))
    lower = bezier((0, 0), (0, -0.07 * c), (0.5 * c, -0.035 * c), (c, 0))
    th = math.radians(ang_deg)
    off = 0.35 * c  # pitch axis location along chord

    def to3d(p):
        u = p[0] - off
        v = p[1]
        y = u * math.cos(th) - v * math.sin(th)
        z = u * math.sin(th) + v * math.cos(th)
        return cq.Vector(x, y, z)

    e1 = cq.Edge.makeSpline([to3d(p) for p in upper])
    e2 = cq.Edge.makeSpline([to3d(p) for p in lower])
    return cq.Wire.assembleEdges([e1, e2])


wires = [section(r_root - 3.0, root_chord, root_ang)]
n = 6
for i in range(n + 1):
    f = i / n
    x = r_root + f * blade_len
    chord = root_chord + f * (tip_chord - root_chord)
    ang = root_ang + f * (tip_ang - root_ang)
    wires.append(section(x, chord, ang))

blade = cq.Solid.makeLoft(wires, False)

result = hub.union(cq.Workplane("XY").add(blade))
