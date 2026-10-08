import cadquery as cq
import math

# Basic dimensions
D = 30.0
R = D / 2.0
L = 60.0

# Knurl parameters
n_grooves = 12          # grooves per direction
pitch = 150.0           # helix pitch (gives ~32 deg helix angle)
depth = 1.0             # V-notch depth
half_w = 0.8            # half width of V-notch at surface
ext = 5.0               # path extension beyond the part ends

# Base cylinder along Z
body = cq.Workplane("XY").circle(R).extrude(L)


def make_groove(lefthand):
    # Helical path starting at (R, 0, -ext)
    helix = cq.Wire.makeHelix(pitch, L + 2 * ext, R, lefthand=lefthand)
    helix = helix.translate(cq.Vector(0, 0, -ext))
    # V-shaped notch profile in the XZ plane at the helix start
    z0 = -ext
    profile = (
        cq.Workplane("XZ")
        .polyline([
            (R + 0.5, z0 - half_w),
            (R + 0.5, z0 + half_w),
            (R - depth, z0),
        ])
        .close()
    )
    groove = profile.sweep(cq.Workplane("XY").add(helix), isFrenet=True)
    return groove.val()


result = body
for lh in (False, True):
    g = make_groove(lh)
    for i in range(n_grooves):
        ang = 360.0 / n_grooves * i
        gi = g.rotate(cq.Vector(0, 0, 0), cq.Vector(0, 0, 1), ang)
        result = result.cut(cq.Workplane("XY").add(gi))
