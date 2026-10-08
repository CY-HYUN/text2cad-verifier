import cadquery as cq
import math

D = 40.0
R = D / 2.0
L = 100.0
amp = 30.0
groove_w = 6.0
depth = 4.0

# Base cylinder on Front (XZ) plane, symmetric extrusion -> axis along Y
body = cq.Workplane("XZ").circle(R).extrude(L / 2.0, both=True)

# Sine cam groove: y = amp*sin(theta), one period around the circumference.
# Built as a dense series of radial cutters of groove width (approximates sweep cut).
N = 360
r_in = R - depth
cut_len = depth + 2.0
tools = []
for i in range(N):
    th = 2 * math.pi * i / N
    y = amp * math.sin(th)
    d = cq.Vector(math.cos(th), 0, math.sin(th))
    p = cq.Vector(r_in * math.cos(th), y, r_in * math.sin(th))
    tools.append(cq.Solid.makeCylinder(groove_w / 2.0, cut_len, p, d))

cutter = cq.Compound.makeCompound(tools)
result = body.cut(cq.Workplane().add(cutter))
