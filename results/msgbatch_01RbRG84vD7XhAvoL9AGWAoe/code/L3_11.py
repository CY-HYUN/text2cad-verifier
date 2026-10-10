import cadquery as cq
import math

P0 = cq.Vector(0, 0, 0)
P1 = cq.Vector(0, 0, 60)
P2 = cq.Vector(60, 0, 60)
P3 = cq.Vector(60, 0, 120)

def bez(t):
    u = 1 - t
    return P0 * (u**3) + P1 * (3 * u * u * t) + P2 * (3 * u * t * t) + P3 * (t**3)

wall = 3.0

def frame(t):
    s = t * t * (3 - 2 * t)  # smooth blend of tilt
    a = math.radians(45.0) * s
    n = cq.Vector(math.sin(a), 0, math.cos(a))
    xd = cq.Vector(math.cos(a), 0, -math.sin(a))
    return n, xd

def section(t, off=0.0, shift=0.0):
    c = bez(t)
    n, xd = frame(t)
    c = c + n * shift
    rx = 60 - 30 * t - off
    ry = 40 - 10 * t - off
    if abs(rx - ry) < 1e-6:
        return cq.Wire.assembleEdges([cq.Edge.makeCircle(rx, c, n)])
    return cq.Wire.makeEllipse(rx, ry, c, n, xd)

N = 10
ts = [i / N for i in range(N + 1)]

outer_wires = [section(t) for t in ts]
inner_wires = [section(t, wall) for t in ts]
# extend inner slightly beyond both ends for clean openings
inner_wires[0] = section(0.0, wall, -1.0)
inner_wires[-1] = section(1.0, wall, 1.0)

outer = cq.Solid.makeLoft(outer_wires)
inner = cq.Solid.makeLoft(inner_wires)
body = outer.cut(inner)

# Flange lip at top inclined port
n_top, _ = frame(1.0)
c_top = bez(1.0)
r_out_top = 30.0
flange = cq.Solid.makeCylinder(r_out_top + 5.0, 2.0, c_top, n_top)
flange_hole = cq.Solid.makeCylinder(r_out_top - wall, 6.0, c_top - n_top * 2.0, n_top)
flange = flange.cut(flange_hole)

result = cq.Workplane("XY").add(body.fuse(flange).clean())
