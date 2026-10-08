import cadquery as cq
import math

R = 20.0          # cylinder radius (dia 40)
L = 100.0         # cylinder length (symmetric)
amp = 30.0        # sine amplitude (axial)
w = 6.0           # groove width
depth = 4.0       # groove depth

# Base cylinder on Front plane, symmetric extrusion -> axis along Y, from -50 to +50
body = cq.Workplane("XZ").circle(R).extrude(L / 2.0, both=True)

# Build groove tool as a ring of ruled segments following the wrapped sine curve
N = 90
r_in = R - depth
r_out = R + 1.0  # overshoot for a clean cut

def section(theta):
    yc = amp * math.sin(theta)
    c, s = math.cos(theta), math.sin(theta)
    pts = [
        (r_in * c, yc - w / 2, r_in * s),
        (r_out * c, yc - w / 2, r_out * s),
        (r_out * c, yc + w / 2, r_out * s),
        (r_in * c, yc + w / 2, r_in * s),
    ]
    vs = [cq.Vector(*p) for p in pts]
    vs.append(vs[0])
    return cq.Wire.makePolygon(vs)

segments = []
for i in range(N):
    t0 = 2 * math.pi * i / N
    t1 = 2 * math.pi * (i + 1) / N
    seg = cq.Solid.makeLoft([section(t0), section(t1)], True)
    segments.append(seg)

tool = segments[0]
for s in segments[1:]:
    tool = tool.fuse(s)
tool = tool.clean()

result = body.cut(tool)
