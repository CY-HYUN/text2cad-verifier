import cadquery as cq
import math

R = 15.0
L = 60.0
pitch = 40.0
n = 12
depth = 1.0
hw = 1.0
ext = 5.0
H = L + 2 * ext

body = cq.Workplane("XY").circle(R).extrude(L)

def groove(left):
    helix = cq.Wire.makeHelix(pitch, H, R, center=cq.Vector(0, 0, -ext), dir=cq.Vector(0, 0, 1), lefthand=left)
    path = cq.Workplane("XY").add(helix)
    prof = (cq.Workplane("XZ", origin=(0, 0, -ext))
            .polyline([(R + depth, -2 * hw), (R + depth, 2 * hw), (R - depth, 0)])
            .close())
    return prof.sweep(path, isFrenet=True)

for left in (False, True):
    g = groove(left).val()
    for i in range(n):
        gi = g.rotate(cq.Vector(0, 0, 0), cq.Vector(0, 0, 1), i * 360.0 / n)
        body = body.cut(cq.Workplane("XY").add(gi))

result = body
