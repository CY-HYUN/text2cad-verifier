import cadquery as cq
import math

# Longitudinal spine: cubic Bezier in XZ plane
P0 = (0.0, 0.0)
P1 = (20.0, 35.0)
P2 = (80.0, 35.0)
P3 = (110.0, 0.0)

def bez(t):
    a = (1 - t) ** 3
    b = 3 * (1 - t) ** 2 * t
    c = 3 * (1 - t) * t ** 2
    d = t ** 3
    x = a * P0[0] + b * P1[0] + c * P2[0] + d * P3[0]
    z = a * P0[1] + b * P1[1] + c * P2[1] + d * P3[1]
    return x, z

L = 110.0
k = math.log(0.5) / math.log(1.0 / 3.0)  # maps rear third to mid

def width(x):
    s = min(max(x / L, 1e-4), 1 - 1e-4)
    u = s ** k
    return 18.0 + 42.0 * math.sin(math.pi * u) ** 0.7

base_h = 2.0
wires = []
ts = [0.04 + i * (0.92 / 13) for i in range(14)]
for t in ts:
    x, z = bez(t)
    h = z + base_h
    w = width(x)
    off = 0.06 * w  # asymmetric bias of the crown toward the right side
    prof = [
        (-0.44 * w, 0.0),
        (-0.50 * w, 0.22 * h),
        (-0.43 * w, 0.60 * h),
        (-0.22 * w + off, 0.92 * h),
        (off, h),
        (0.24 * w + off, 0.90 * h),
        (0.45 * w, 0.55 * h),
        (0.50 * w, 0.20 * h),
        (0.44 * w, 0.0),
    ]
    pts = [cq.Vector(x, y, zz) for (y, zz) in prof]
    sp = cq.Edge.makeSpline(pts)
    ln = cq.Edge.makeLine(pts[-1], pts[0])
    wires.append(cq.Wire.assembleEdges([sp, ln]))

body = cq.Solid.makeLoft(wires, True)
result = cq.Workplane("XY").add(body)

# Concave thumb rest on the left side (negative Y)
xt = 42.0
wt = width(xt)
thumb = cq.Workplane("XY").add(
    cq.Solid.makeSphere(26.0, cq.Vector(xt, -wt / 2 - 19.0, 11.0), angleDegrees1=-90, angleDegrees2=90)
)
try:
    result = result.cut(thumb)
except Exception:
    pass

# Hollow it out as a cover, open at the bottom
try:
    shelled = result.faces("<Z").shell(-1.6)
    if shelled.val().isValid():
        result = shelled
except Exception:
    pass
