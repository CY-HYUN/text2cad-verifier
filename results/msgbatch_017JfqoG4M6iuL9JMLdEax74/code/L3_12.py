import cadquery as cq
import math

R = 40.0
H_center = 60.0          # height of inclined-surface center on the axis
tilt = 30.0

# Base cylinder (made tall, then trimmed by the inclined plane)
body = cq.Workplane("XY").circle(R).extrude(120)

# Inclined cutting plane: normal (0, sin30, cos30) -> highest point at -Y
cutter = (cq.Workplane("XY")
          .box(400, 400, 300, centered=(True, True, False))
          .rotate((0, 0, 0), (1, 0, 0), -tilt)
          .translate((0, 0, H_center)))
body = body.cut(cutter)

# Paraboloid recess: x^2 + y^2 = 40 z, opening diameter 60 -> depth 22.5
rim_r = 30.0
depth = rim_r ** 2 / 40.0
pts = [(r, r * r / 40.0) for r in [i * rim_r / 30.0 for i in range(31)]]
prof = (cq.Workplane("XZ")
        .moveTo(0, 0)
        .spline(pts[1:], includeCurrent=True)
        .lineTo(rim_r, depth + 30)
        .lineTo(0, depth + 30)
        .close())
para = prof.revolve(360, (0, 0, 0), (0, 1, 0))
para = (para.translate((0, 0, -depth))
        .rotate((0, 0, 0), (1, 0, 0), -tilt)
        .translate((0, 0, H_center)))
body = body.cut(para)

# Sine-wave groove on the side wall
N = 6
amp = 5.0
zc = 30.0
gr = 2.0
npts = 144
path_pts = []
for i in range(npts):
    t = 2 * math.pi * i / npts
    path_pts.append((R * math.cos(t), R * math.sin(t), zc + amp * math.sin(N * t)))

groove = None
try:
    path = cq.Workplane("XY").spline(path_pts, periodic=True)
    tan = cq.Vector(0, R, amp * N).normalized()
    plane = cq.Plane(origin=path_pts[0], xDir=(1, 0, 0), normal=tan.toTuple())
    groove = cq.Workplane(plane).circle(gr).sweep(path, isFrenet=False)
    if not groove.val().isValid():
        groove = None
except Exception:
    groove = None

if groove is not None:
    try:
        body = body.cut(groove)
    except Exception:
        groove = None

if groove is None:
    # Fallback: chain of spheres approximating the swept groove
    m = 360
    sph = None
    for i in range(m):
        t = 2 * math.pi * i / m
        p = (R * math.cos(t), R * math.sin(t), zc + amp * math.sin(N * t))
        s = cq.Workplane("XY").sphere(gr).translate(p)
        sph = s if sph is None else sph.union(s)
    body = body.cut(sph)

result = body
