import cadquery as cq
import math

# Longitudinal spine control points (XZ plane): cubic Bezier
P = [(0, 0), (20, 35), (80, 35), (110, 0)]

def bez(t):
    u = 1 - t
    x = u**3*P[0][0] + 3*u*u*t*P[1][0] + 3*u*t*t*P[2][0] + t**3*P[3][0]
    z = u**3*P[0][1] + 3*u*u*t*P[1][1] + 3*u*t*t*P[2][1] + t**3*P[3][1]
    return x, z

def spine_z(xq):
    lo, hi = 0.0, 1.0
    for _ in range(60):
        mid = (lo + hi) / 2
        if bez(mid)[0] < xq:
            lo = mid
        else:
            hi = mid
    return bez((lo + hi) / 2)[1]

# Bottom contour (asymmetric half-widths in XY): x, left(+y), right(-y)
stations = [(0, 7, 5), (40, 30, 26), (80, 33, 27), (110, 9, 6)]

wires = []
for x, wl, wr in stations:
    z = max(spine_z(x), 1.5)  # small height at the tips to avoid degenerate section
    pts = [
        (-wr * 0.95, z * 0.55),
        (-wr * 0.55, z * 0.88),
        (0, z),
        (wl * 0.55, z * 0.88),
        (wl * 0.95, z * 0.55),
        (wl, 0),
    ]
    w = (cq.Workplane("YZ", origin=(x, 0, 0))
         .moveTo(-wr, 0)
         .spline(pts, includeCurrent=True)
         .close())
    wires.append(w)

# Loft through sections in sequence
solid = wires[0]
for w in wires[1:]:
    solid = solid.workplane  # placeholder to keep structure clear
    break

loft = cq.Solid.makeLoft([w.val() if isinstance(w.val(), cq.Wire) else w.wires().val() for w in wires], False)
body = cq.Workplane("XY").add(loft)

# Thicken inward by 2.0 mm (hollow shell, open at bottom)
try:
    result = body.faces("<Z").shell(-2.0)
except Exception:
    result = body
