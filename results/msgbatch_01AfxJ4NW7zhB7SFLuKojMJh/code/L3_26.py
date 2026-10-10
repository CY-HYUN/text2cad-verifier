import cadquery as cq
import math

R_MIN, R_MAX = 50.0, 90.0
H = R_MAX - R_MIN
T = 15.0
PITCH = 20.0
BORE = 25.0
KEY_W, KEY_D = 6.0, 6.0

def disp(theta_deg):
    # normalized displacement: rise 0-90, return 90-180, dwell 180-360
    t = theta_deg % 360.0
    def cyc(u):
        # smooth sine-based (cycloidal-type) blend
        return u - math.sin(2 * math.pi * u) / (2 * math.pi)
    if t < 90:
        return cyc(t / 90.0)
    elif t < 180:
        return 1.0 - cyc((t - 90) / 90.0)
    return 0.0

def r_main(th):
    return R_MIN + H * disp(th)

def r_sec(th):
    # conjugate (constant-breadth) profile
    return 2 * (R_MIN + R_MAX) / 2 + 0 - r_main(th + 180.0)

def make_cam(rfun, z0):
    n = 120
    pts = []
    for i in range(n):
        a = 360.0 * i / n
        r = rfun(a)
        pts.append((r * math.cos(math.radians(a)), r * math.sin(math.radians(a))))
    cam = (cq.Workplane("XY").workplane(offset=z0)
           .spline(pts, periodic=True).close().extrude(T))
    bore = (cq.Workplane("XY").workplane(offset=z0 - 1)
            .circle(BORE / 2).extrude(T + 2))
    cam = cam.cut(bore)
    try:
        cam = cam.faces(">Z or <Z").edges().chamfer(1.0)
    except Exception:
        pass
    key = (cq.Workplane("XY").workplane(offset=z0 - 1)
           .center((BORE / 2 + KEY_D) / 2 - 3, 0)
           .rect(BORE / 2 + KEY_D + 6, KEY_W).extrude(T + 2))
    cam = cam.cut(key)
    return cam

cam1 = make_cam(r_main, 0.0)
cam2 = make_cam(r_sec, PITCH)

result = cam1.union(cam2)
