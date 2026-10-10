import cadquery as cq
import math

N = 72

def section(z, r_func):
    pts = []
    for i in range(N):
        t = 2 * math.pi * i / N
        r = r_func(t)
        pts.append(cq.Vector(r * math.cos(t), r * math.sin(t), z))
    edge = cq.Edge.makeSpline(pts, periodic=True)
    return cq.Wire.assembleEdges([edge])

# Bottom: circle D60
w0 = section(0.0, lambda t: 30.0)
# Middle: six-peak sinusoidal ring, mean D70, amplitude 5, peak on +X
w1 = section(75.0, lambda t: 35.0 + 5.0 * math.cos(6 * t))
# Top: circle D80
w2 = section(150.0, lambda t: 40.0)

solid = cq.Solid.makeLoft([w0, w1, w2], False)
result = cq.Workplane("XY").add(solid)
