import cadquery as cq
import math

a = 100.0   # inner semi-major (radius)
b = 50.0    # inner semi-minor (depth)
t = 8.0     # wall thickness
h_str = 25.0

N = 24
inner_pts = []
outer_pts = []
for i in range(N + 1):
    th = math.radians(90.0 * i / N)
    x = a * math.cos(th)
    z = b * math.sin(th)
    nx, nz = math.cos(th) / a, math.sin(th) / b
    L = math.hypot(nx, nz)
    nx, nz = nx / L, nz / L
    inner_pts.append((x, z))
    outer_pts.append((x + t * nx, z + t * nz))

# inner goes from (a,0) to (0,b); outer goes from (0,b+t) back to (a+t,0)
outer_rev = list(reversed(outer_pts))

prof = (
    cq.Workplane("XZ")
    .moveTo(a, -h_str)
    .lineTo(a, 0)
    .spline(inner_pts[1:], tangents=[(0, 1), (-1, 0)], includeCurrent=True)
    .lineTo(outer_rev[0][0], outer_rev[0][1])
    .spline(outer_rev[1:], tangents=[(1, 0), (0, -1)], includeCurrent=True)
    .lineTo(a + t, -h_str)
    .close()
)
head = prof.revolve(360, (0, 0, 0), (0, 1, 0))

# Nozzle / flange at the vertex
z_top = b + t + 30.0
z_base = 52.0
nozzle = (
    cq.Workplane("XY")
    .workplane(offset=z_base)
    .circle(20.0)
    .extrude(z_top - z_base)
)
body = head.union(nozzle)

bore = (
    cq.Workplane("XY")
    .workplane(offset=30.0)
    .circle(15.0)
    .extrude(z_top - 30.0 + 1.0)
)
result = body.cut(bore)
