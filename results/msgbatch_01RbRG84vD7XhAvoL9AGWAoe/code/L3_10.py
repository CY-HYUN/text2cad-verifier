import cadquery as cq
import math

t = 5.0          # wall thickness
z_top = 75.0     # inner paraboloid rim height (outer bottom at z=-5 -> total height 80)
R_out = 85.0     # max outer radius (diameter 170)
fl_t = 5.0       # flange thickness
z_fl_bot = z_top - fl_t

def inner(r):
    return (r, r * r / 80.0)

def outer(r):
    s = math.sqrt(1 + (r / 40.0) ** 2)
    return (r + t * (r / 40.0) / s, r * r / 80.0 - t / s)

r_in_top = math.sqrt(80.0 * z_top)

# find inner parameter where the outer offset curve reaches the flange bottom
lo, hi = 0.0, r_in_top
for _ in range(60):
    mid = 0.5 * (lo + hi)
    if outer(mid)[1] < z_fl_bot:
        lo = mid
    else:
        hi = mid
r_join = 0.5 * (lo + hi)

N = 30
inner_pts = [inner(r_in_top * i / N) for i in range(1, N + 1)]
outer_pts = [outer(r_join * i / N) for i in range(N, -1, -1)]

prof = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .spline(inner_pts, includeCurrent=True)
    .lineTo(R_out, z_top)
    .lineTo(R_out, z_fl_bot)
    .lineTo(*outer_pts[0])
    .spline(outer_pts[1:], includeCurrent=True)
    .close()
)
body = prof.revolve(360, (0, 0, 0), (0, 1, 0))

# central light-source hole
hole = cq.Workplane("XY").workplane(offset=-20).circle(5.0).extrude(40)
body = body.cut(hole)

# four flange mounting holes, one on +Y
r_h = 82.3
pts = [(r_h * math.cos(math.radians(90 + 90 * k)), r_h * math.sin(math.radians(90 + 90 * k))) for k in range(4)]
fh = (
    cq.Workplane("XY").workplane(offset=z_fl_bot - 0.01)
    .pushPoints(pts).circle(2.5).extrude(fl_t + 0.02)
)
result = body.cut(fh)
