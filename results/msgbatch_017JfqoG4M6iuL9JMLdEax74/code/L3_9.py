import cadquery as cq
import math

N = 72  # sample points per section

def section(z, r_mean, amp, lobes=6):
    pts = []
    for i in range(N):
        t = 2 * math.pi * i / N
        r = r_mean + amp * math.cos(lobes * t)  # peak on +X at t=0
        pts.append(cq.Vector(r * math.cos(t), r * math.sin(t), z))
    edge = cq.Edge.makeSpline(pts, periodic=True)
    return cq.Wire.assembleEdges([edge])

w_bottom = section(0.0, 30.0, 0.0)    # circle D60
w_mid = section(75.0, 35.0, 5.0)      # six-petal sinusoidal ring, mean D70, amp 5
w_top = section(150.0, 40.0, 0.0)     # circle D80

solid = cq.Solid.makeLoft([w_bottom, w_mid, w_top], False)
result = cq.Workplane("XY").add(solid)
