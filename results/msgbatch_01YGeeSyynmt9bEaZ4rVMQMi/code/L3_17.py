import cadquery as cq
import math

D = 50.0
R = D / 2.0
H = 100.0
amp = 15.0
zc = 50.0
half_w = 4.0
depth = 5.0

# Base cylinder
cyl = cq.Workplane("XY").circle(R).extrude(H)

# Unwrapped: X = arc length (0..pi*D), Y = 15*sin(k*X)+50, k = 2*pi/(pi*D)
circ = math.pi * D
k = 2 * math.pi / circ

r_in = R - depth
r_out = R + 1.0  # extend outside to ensure clean cut

N = 144

def section(i):
    theta = 2 * math.pi * i / N
    X = theta * R
    z = amp * math.sin(k * X) + zc
    c, s = math.cos(theta), math.sin(theta)
    pts = [
        cq.Vector(r_in * c, r_in * s, z - half_w),
        cq.Vector(r_out * c, r_out * s, z - half_w),
        cq.Vector(r_out * c, r_out * s, z + half_w),
        cq.Vector(r_in * c, r_in * s, z + half_w),
    ]
    return cq.Wire.makePolygon(pts, close=True)

sections = [section(i) for i in range(N)]
segs = []
for i in range(N):
    w1 = sections[i]
    w2 = sections[(i + 1) % N]
    segs.append(cq.Solid.makeLoft([w1, w2], True))

groove = segs[0]
for s in segs[1:]:
    groove = groove.fuse(s)
groove = groove.clean()

result = cyl.cut(cq.Workplane("XY").add(groove))
