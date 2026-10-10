import cadquery as cq
import math

R0, R1 = 50.0, 90.0
H = R1 - R0
T = 15.0

def r_main(th):
    th = th % 360.0
    if th < 180.0:
        return R0
    if th < 270.0:
        u = (th - 180.0) / 90.0
        return R0 + H * (u - math.sin(2 * math.pi * u) / (2 * math.pi))
    u = (th - 270.0) / 90.0
    return R1 - H * (u - math.sin(2 * math.pi * u) / (2 * math.pi))

def r_conj(th):
    return (R0 + R1) - r_main(th + 180.0)

def pt(r, th):
    a = math.radians(th)
    return (r * math.cos(a), r * math.sin(a))

def pts(fn, a0, a1, step=7.5):
    n = int(round((a1 - a0) / step))
    return [pt(fn(a0 + (a1 - a0) * i / n), a0 + (a1 - a0) * i / n) for i in range(n + 1)]

# main cam profile
p_rise = pts(r_main, 180, 270)
p_ret = pts(r_main, 270, 360)
cam1 = (cq.Workplane("XY")
        .moveTo(*pt(R0, 0))
        .threePointArc(pt(R0, 90), pt(R0, 180))
        .spline(p_rise[1:], includeCurrent=True)
        .spline(p_ret[1:], includeCurrent=True)
        .close()
        .extrude(T))

# conjugate cam profile
q1 = pts(r_conj, 0, 90)
q2 = pts(r_conj, 90, 180)
cam2 = (cq.Workplane("XY").workplane(offset=35.0)
        .moveTo(*pt(R1, 0))
        .spline(q1[1:], includeCurrent=True)
        .spline(q2[1:], includeCurrent=True)
        .threePointArc(pt(R1, 270), pt(R1, 360))
        .close()
        .extrude(T))

# shaft hole with keyway (through both)
hole = cq.Workplane("XY").workplane(offset=-5).circle(12.5).extrude(70)
key = cq.Workplane("XY").workplane(offset=-5).center(0, 12.5 + 6.0 / 2 - 0.0).rect(6.0, 6.0 + 0.0).extrude(70)
cutter = hole.union(key)

def finish(c):
    c = c.cut(cutter)
    try:
        return c.edges().chamfer(1.0)
    except Exception:
        return c

c1 = finish(cam1)
c2 = finish(cam2)
result = c1.union(c2)
