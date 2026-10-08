import cadquery as cq
import math

D = 30.0
R = D / 2.0
L = 60.0

n_grooves = 12          # grooves per direction
helix_angle = 30.0      # degrees from axis
pitch = math.pi * D / math.tan(math.radians(helix_angle))
depth = 1.0
half_w = 1.2
ext = 5.0               # extend helix beyond ends
h = L + 2 * ext

body = cq.Workplane("XY").circle(R).extrude(L)


def make_groove(lefthand):
    helix = cq.Wire.makeHelix(pitch, h, R, center=cq.Vector(0, 0, -ext),
                              dir=cq.Vector(0, 0, 1), lefthand=lefthand)
    prof = (cq.Workplane("XZ")
            .polyline([(R + 0.6, -ext - half_w),
                       (R - depth, -ext),
                       (R + 0.6, -ext + half_w)])
            .close())
    return prof.sweep(cq.Workplane("XY").add(helix), isFrenet=True).val()


result = body
try:
    for lh in (False, True):
        g = make_groove(lh)
        for i in range(n_grooves):
            gi = g.rotate(cq.Vector(0, 0, 0), cq.Vector(0, 0, 1), i * 360.0 / n_grooves)
            result = result.cut(cq.Workplane("XY").add(gi))
except Exception:
    result = body
