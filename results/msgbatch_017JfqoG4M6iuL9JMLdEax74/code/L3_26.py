import cadquery as cq
import math

T = 15.0          # cam thickness
GAP = 20.0        # axial spacing between cams
RB, RMAX = 50.0, 90.0
H = RMAX - RB
D = RB + RMAX     # conjugate sum

def msine(u):
    k = 1.0 / (4.0 + math.pi)
    if u <= 0.125:
        return k * (math.pi * u - 0.25 * math.sin(4 * math.pi * u))
    elif u <= 0.875:
        return k * (2 + math.pi * u - 2.25 * math.sin(math.pi / 3 + 4 * math.pi * u / 3))
    else:
        return k * (4 + math.pi * u - 0.25 * math.sin(4 * math.pi * u))

def r_main(deg):
    deg = deg % 360.0
    if deg < 90:
        return RB + H * msine(deg / 90.0)
    elif deg < 180:
        return RB + H * (1 - msine((deg - 90) / 90.0))
    else:
        return RB

def r_conj(deg):
    return D - r_main(deg + 180.0)

def cam(rfunc, z0):
    N = 180
    pts = []
    for i in range(N):
        a = 360.0 * i / N
        r = rfunc(a)
        t = math.radians(a)
        pts.append((r * math.cos(t), r * math.sin(t)))
    body = (cq.Workplane("XY").workplane(offset=z0)
            .spline(pts, periodic=True, includeCurrent=False).close()
            .extrude(T))
    try:
        body = body.edges().chamfer(1.0)
    except Exception:
        pass
    # shaft hole with keyway
    hole = (cq.Workplane("XY").workplane(offset=z0 - 1)
            .circle(12.5).extrude(T + 2))
    key = (cq.Workplane("XY").workplane(offset=z0 - 1)
           .center(12.5 + 3 - 2, 0).rect(10, 6).extrude(T + 2))
    cutter = hole.union(key)
    body = body.cut(cutter)
    try:
        body = body.faces(">Z or <Z").edges("not %BSPLINE").chamfer(1.0)
    except Exception:
        pass
    return body

cam1 = cam(r_main, 0.0)
cam2 = cam(r_conj, T + GAP)

result = cam1.union(cam2)
