import cadquery as cq
import math

r_min, r_max = 50.0, 90.0
h = r_max - r_min

def msine(x):
    k = 1.0 / (4.0 + math.pi)
    if x <= 0.125:
        return k * (math.pi * x - 0.25 * math.sin(4 * math.pi * x))
    elif x <= 0.875:
        return k * (2 + math.pi * x - 2.25 * math.sin(math.pi / 3 + 4 * math.pi * x / 3))
    else:
        return k * (4 + math.pi * x - 0.25 * math.sin(4 * math.pi * x))

def r1(theta_deg):
    t = theta_deg % 360.0
    if t < 90.0:            # rise
        return r_min + h * msine(t / 90.0)
    elif t < 180.0:         # return
        return r_min + h * (1 - msine((t - 90.0) / 90.0))
    else:                   # dwell
        return r_min

def r2(theta_deg):
    # conjugate: constant sum of radii for two-point contact (opposed followers)
    return (r_min + r_max) - r1(theta_deg + 180.0)

def profile_pts(rf, n=180):
    pts = []
    for i in range(n):
        th = 360.0 * i / n
        r = rf(th)
        a = math.radians(th)
        pts.append((r * math.cos(a), r * math.sin(a)))
    return pts

thk = 15.0
cam1 = (cq.Workplane("XY")
        .spline(profile_pts(r1), periodic=True, includeCurrent=False)
        .close().extrude(thk))

cam2 = (cq.Workplane("XY", origin=(0, 0, 35.0))
        .spline(profile_pts(r2), periodic=True, includeCurrent=False)
        .close().extrude(thk))

# shaft hole with keyway
cutter = (cq.Workplane("XY", origin=(0, 0, -5)).circle(12.5).extrude(70)
          .union(cq.Workplane("XY", origin=(0, 0, -5)).center(0, 14.25)
                 .rect(6.0, 8.5).extrude(70)))

cam1 = cam1.cut(cutter)
cam2 = cam2.cut(cutter)

def chamf(w):
    try:
        return w.edges().chamfer(1.0)
    except Exception:
        try:
            return w.faces(">Z or <Z").edges().chamfer(1.0)
        except Exception:
            return w

cam1 = chamf(cam1)
cam2 = chamf(cam2)

result = cam1.union(cam2)
