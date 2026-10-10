import cadquery as cq
import math

T = 15.0
GAP = 20.0
RB, RMAX = 50.0, 90.0
H = RMAX - RB
HOLE_D = 25.0
KW, KD = 6.0, 6.0

def msine(x):
    if x < 0.125:
        return 0.43990085 * x - 0.0350062 * math.sin(4 * math.pi * x)
    elif x < 0.875:
        return 0.28004957 + 0.43990085 * x - 0.31505577 * math.cos(4 * math.pi * x / 3 - math.pi / 6)
    else:
        return 0.56009915 + 0.43990085 * x - 0.0350062 * math.sin(4 * math.pi * x)

def r_main(deg):
    d = deg % 360.0
    if d < 90:
        return RB + H * msine(d / 90.0)
    elif d < 180:
        return RB + H * (1 - msine((d - 90) / 90.0))
    return RB

def r_conj(deg):
    # conjugate: constant sum of opposed radii -> dual-point contact
    return (RB + RMAX) - r_main(deg + 180.0)

def cam(rfunc, z0):
    pts = []
    N = 240
    for i in range(N):
        a = 360.0 * i / N
        r = rfunc(a)
        pts.append((r * math.cos(math.radians(a)), r * math.sin(math.radians(a))))
    body = (cq.Workplane("XY").workplane(offset=z0)
            .spline(pts, periodic=True).close().extrude(T))
    hole = (cq.Workplane("XY").workplane(offset=z0 - 1)
            .circle(HOLE_D / 2).extrude(T + 2))
    key = (cq.Workplane("XY").workplane(offset=z0 - 1)
           .center((HOLE_D / 2 + KD) / 2, 0)
           .rect(HOLE_D / 2 + KD, KW).extrude(T + 2))
    body = body.cut(hole).cut(key)
    try:
        body = body.edges("not |Z").chamfer(1.0)
    except Exception:
        try:
            body = body.faces(">Z or <Z").edges().chamfer(1.0)
        except Exception:
            pass
    return body

cam1 = cam(r_main, 0.0)
cam2 = cam(r_conj, T + GAP)

result = cam1.union(cam2)
