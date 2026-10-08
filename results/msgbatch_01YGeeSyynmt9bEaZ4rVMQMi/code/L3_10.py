import cadquery as cq
import math

t = 5.0
H = 80.0

# Inner parabola z = r^2/80, r 0..80
N = 40
inner = [(80.0 * i / N, (80.0 * i / N) ** 2 / 80.0) for i in range(N + 1)]

# Outer offset curve (normal offset outward by t), extended past the top for clipping
outer = []
rmax_ext = 88.0
for i in range(N + 1):
    r = rmax_ext * i / N
    z = r * r / 80.0
    nx, nz = r / 40.0, -1.0
    n = math.hypot(nx, nz)
    outer.append((r + t * nx / n, z + t * nz / n))
outer_rev = list(reversed(outer))

prof = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .spline(inner[1:], includeCurrent=True)
    .lineTo(inner[-1][0], outer_rev[0][1])
    .lineTo(outer_rev[0][0], outer_rev[0][1])
    .spline(outer_rev[1:], includeCurrent=True)
    .close()
)
shell = prof.revolve(360, (0, 0, 0), (0, 1, 0))

# Clip to top at z = H
clip = cq.Workplane("XY").box(400, 400, H + 50, centered=(True, True, False)).translate((0, 0, -40))
shell = shell.intersect(clip)

# Flange: ring at top, 5 mm thick, out to R95
flange = (
    cq.Workplane("XY").workplane(offset=H - 5.0)
    .circle(95.0).circle(80.0).extrude(5.0)
)
body = shell.union(flange)

# Mounting holes on R90, one at +Y
pts = [(90 * math.cos(math.radians(90 + 90 * k)), 90 * math.sin(math.radians(90 + 90 * k))) for k in range(4)]
holes = (
    cq.Workplane("XY").workplane(offset=H - 10.0)
    .pushPoints(pts).circle(2.5).extrude(20.0)
)
body = body.cut(holes)

# Central light source hole
lh = cq.Workplane("XY").workplane(offset=-20).circle(5.0).extrude(25.0)
body = body.cut(lh)

result = body
