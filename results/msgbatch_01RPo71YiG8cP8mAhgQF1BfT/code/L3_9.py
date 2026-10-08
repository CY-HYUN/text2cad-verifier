import cadquery as cq
import math

N = 72  # sample points per section

def peak(z):
    # peak radius: 30 -> 40 smoothly over [0,75], then held at 40
    if z <= 75.0:
        return 30.0 + 10.0 * math.sin(math.pi * z / 150.0)
    return 40.0

def valley(z):
    # valley radius: held at 30 over [0,75], then 30 -> 40 smoothly
    if z <= 75.0:
        return 30.0
    return 30.0 + 5.0 * (1.0 - math.cos(math.pi * (z - 75.0) / 75.0))

def section(z, lobes=6):
    p, v = peak(z), valley(z)
    r_mean = 0.5 * (p + v)
    amp = 0.5 * (p - v)
    if amp < 1e-6:
        return cq.Wire.assembleEdges(
            [cq.Edge.makeCircle(r_mean, cq.Vector(0, 0, z), cq.Vector(0, 0, 1))]
        )
    pts = []
    for i in range(N):
        t = 2 * math.pi * i / N
        r = r_mean + amp * math.cos(lobes * t)  # peak on +X at t=0
        pts.append(cq.Vector(r * math.cos(t), r * math.sin(t), z))
    edge = cq.Edge.makeSpline(pts, periodic=True)
    return cq.Wire.assembleEdges([edge])

n_sec = 20
zs = [150.0 * i / n_sec for i in range(n_sec + 1)]
wires = [section(z) for z in zs]

solid = cq.Solid.makeLoft(wires, False)
result = cq.Workplane("XY").add(solid)
