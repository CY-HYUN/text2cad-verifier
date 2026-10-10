import cadquery as cq
import math

R_OUT = 25.0
L = 100.0
AMP = 15.0
MID = 50.0
GR = 4.0          # groove half-width / bottom radius
DEPTH = 5.0
R_BOTTOM_CENTER = R_OUT - DEPTH + GR  # 24? -> center of semicircle
# depth 5 with radius 4 bottom: semicircle center at r = 25 - 5 + 4 = 24
# (lowest point at r = 20)

body = cq.Workplane("XY").circle(R_OUT).extrude(L)

def make_path(R, n=96):
    pts = []
    for i in range(n):
        t = 2 * math.pi * i / n
        pts.append(cq.Vector(R * math.cos(t), R * math.sin(t), AMP * math.sin(t) + MID))
    e = cq.Edge.makeSpline(pts, periodic=True)
    return cq.Wire.assembleEdges([e])

def make_tube(R):
    path = make_path(R)
    origin = cq.Vector(R, 0, MID)
    normal = cq.Vector(0, R, AMP)  # tangent at t=0
    plane = cq.Plane(origin=origin, xDir=cq.Vector(1, 0, 0), normal=normal)
    return cq.Workplane(plane).circle(GR).sweep(cq.Workplane().add(path))

# Stack of tubes from the semicircle bottom outward -> U-shaped cross-section
radii = []
r = R_BOTTOM_CENTER
while r < R_OUT + GR + 0.5:
    radii.append(r)
    r += 1.0

result = body
for rr in radii:
    try:
        result = result.cut(make_tube(rr))
    except Exception:
        pass
