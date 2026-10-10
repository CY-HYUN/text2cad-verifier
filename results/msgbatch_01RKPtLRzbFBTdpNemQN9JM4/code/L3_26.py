import cadquery as cq
import math

R0, H = 50.0, 40.0
T = 15.0
GAP = 20.0
C = 140.0  # constant breadth for the conjugate (2*R0 + H)

def r_main(deg):
    d = deg % 360.0
    if d < 90:
        u = d / 90.0
        s = u - math.sin(2 * math.pi * u) / (2 * math.pi)
        return R0 + H * s
    elif d < 180:
        u = (d - 90) / 90.0
        s = u - math.sin(2 * math.pi * u) / (2 * math.pi)
        return R0 + H * (1 - s)
    return R0

def r_sec(deg):
    return C - r_main(deg + 180.0)

def cam(rf, z0):
    n = 180
    pts = []
    for i in range(n):
        a = 360.0 * i / n
        r = rf(a)
        pts.append((r * math.cos(math.radians(a)), r * math.sin(math.radians(a))))
    body = (cq.Workplane("XY").workplane(offset=z0)
            .spline(pts, periodic=True).close().extrude(T))
    hole = (cq.Workplane("XY").workplane(offset=z0 - 1).circle(12.5).extrude(T + 2))
    key = (cq.Workplane("XY").workplane(offset=z0 - 1)
           .center(9.25, 0).rect(18.5, 6).extrude(T + 2))
    body = body.cut(hole.union(key))
    try:
        body = body.edges().chamfer(1.0)
    except Exception:
        pass
    return body

main_cam = cam(r_main, 0.0)
sec_cam = cam(r_sec, T + GAP)

result = main_cam.union(sec_cam)
