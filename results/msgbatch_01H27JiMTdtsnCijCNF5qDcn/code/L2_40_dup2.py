import cadquery as cq
import math

R = 15.0
L = 60.0
depth = 0.8
half_w = 1.0
pitch = 40.0
ext = 5.0
H = L + 2 * ext
n = 12

body = cq.Workplane("XY").circle(R).extrude(L)

def groove(left):
    helix = cq.Wire.makeHelix(pitch, H, R, lefthand=left).translate(cq.Vector(0, 0, -ext))
    pts = [(R - depth, -ext), (R + 0.7, -ext - half_w - 0.3), (R + 0.7, -ext + half_w + 0.3)]
    prof = cq.Workplane("XZ").polyline(pts).close()
    return prof.sweep(cq.Workplane(obj=helix), isFrenet=True).val()

result = body
for left in (False, True):
    g = groove(left)
    for i in range(n):
        gi = g.rotate(cq.Vector(0, 0, 0), cq.Vector(0, 0, 1), i * 360.0 / n)
        result = result.cut(cq.Workplane(obj=gi))
