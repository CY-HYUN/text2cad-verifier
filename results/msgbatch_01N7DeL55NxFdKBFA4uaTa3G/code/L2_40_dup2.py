import cadquery as cq
import math

# Cylinder parameters
D = 30.0
R = D / 2.0
L = 60.0

# Knurl parameters
n_grooves = 12          # grooves per direction
helix_angle = 30.0      # degrees from axis
depth = 0.8             # groove depth
half_w = 0.7            # half width of V at surface
ext = 5.0               # extension beyond ends

pitch = 2 * math.pi * R / math.tan(math.radians(helix_angle))
height = L + 2 * ext

# Base cylinder along Z
result = cq.Workplane("XY").circle(R).extrude(L)


def groove_solid(lefthand):
    helix = cq.Wire.makeHelix(pitch, height, R, lefthand=lefthand)
    helix = helix.translate(cq.Vector(0, 0, -ext))
    path = cq.Workplane("XY").add(helix)
    # V-shaped profile in XZ plane at helix start point (R, 0, -ext)
    pts = [
        (R + 0.6, -ext - half_w - 0.3),
        (R + 0.6, -ext + half_w + 0.3),
        (R, -ext + half_w),
        (R - depth, -ext),
        (R, -ext - half_w),
    ]
    prof = cq.Workplane("XZ").polyline(pts).close()
    return prof.sweep(path, isFrenet=True).val()


for lh in (False, True):
    try:
        g = groove_solid(lh)
        for i in range(n_grooves):
            ang = 360.0 * i / n_grooves
            gi = g.rotate(cq.Vector(0, 0, 0), cq.Vector(0, 0, 1), ang)
            try:
                result = result.cut(cq.Workplane("XY").add(gi))
            except Exception:
                pass
    except Exception:
        pass
