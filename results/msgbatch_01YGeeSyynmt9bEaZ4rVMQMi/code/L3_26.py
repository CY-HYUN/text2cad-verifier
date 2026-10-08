import cadquery as cq
import math

R_BASE = 50.0
R_MAX = 90.0
H = R_MAX - R_BASE
T = 15.0
Z2 = 35.0


def modsine(x):
    # Modified sine displacement law, normalised 0..1
    if x <= 0.125:
        return 0.43990085 * (x - math.sin(4 * math.pi * x) / (4 * math.pi))
    elif x <= 0.875:
        return 0.28004957 + 0.43990085 * x - 0.31505577 * math.cos(4 * math.pi / 3 * x - math.pi / 6)
    else:
        return 1.0 - modsine(1.0 - x)


def r_main(theta_deg):
    t = theta_deg % 360.0
    if t < 90.0:  # rise
        return R_BASE + H * modsine(t / 90.0)
    elif t < 180.0:  # return
        return R_BASE + H * (1.0 - modsine((t - 90.0) / 90.0))
    else:  # 180 deg dwell
        return R_BASE


def r_conj(theta_deg):
    # Constant-sum conjugate (two-point contact, opposed rollers)
    return (R_BASE + R_MAX) - r_main(theta_deg + 180.0)


def cam_solid(rfunc, z0):
    pts = []
    for i in range(0, 360, 2):
        a = math.radians(i)
        r = rfunc(i)
        pts.append(cq.Vector(r * math.cos(a), r * math.sin(a), z0))
    edge = cq.Edge.makeSpline(pts, periodic=True)
    wire = cq.Wire.assembleEdges([edge])
    face = cq.Face.makeFromWires(wire)
    solid = cq.Solid.extrudeLinear(face, cq.Vector(0, 0, T))
    return cq.Workplane("XY").add(solid)


main = cam_solid(r_main, 0.0)
sec = cam_solid(r_conj, Z2)

# Shaft hole with keyway (through both cams)
hole = cq.Workplane("XY").workplane(offset=-1).circle(12.5).extrude(Z2 + T + 2)
key = (cq.Workplane("XY").workplane(offset=-1)
       .center(12.5 + 6.0 - 4.0, 0).rect(8.0, 6.0).extrude(Z2 + T + 2))
cutter = hole.union(key)

main = main.cut(cutter)
sec = sec.cut(cutter)


def chamfer_all(wp):
    try:
        return wp.edges().chamfer(1.0)
    except Exception:
        try:
            return wp.edges("not |Z").chamfer(1.0)
        except Exception:
            return wp


main = chamfer_all(main)
sec = chamfer_all(sec)

result = main.union(sec)
