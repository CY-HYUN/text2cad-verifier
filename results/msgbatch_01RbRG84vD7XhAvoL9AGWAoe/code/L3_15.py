import cadquery as cq
import math

a, b = 100.0, 50.0      # inner semi-axes (radius, depth)
t_w = 8.0               # wall thickness
h_st = 25.0             # straight cylindrical section height
N = 40

# Inner ellipse points (from equator to apex)
inner = []
outer = []
for i in range(N + 1):
    t = (math.pi / 2) * i / N
    x = a * math.cos(t)
    y = b * math.sin(t)
    nx, ny = x / a**2, y / b**2
    L = math.hypot(nx, ny)
    nx, ny = nx / L, ny / L
    inner.append((x, y))
    outer.append((x + t_w * nx, y + t_w * ny))

# Ensure exact endpoints
inner[0] = (a, 0.0); inner[-1] = (0.0, b)
outer[0] = (a + t_w, 0.0); outer[-1] = (0.0, b + t_w)

inner_rev = list(reversed(inner))

prof = (
    cq.Workplane("XY")
    .moveTo(a + t_w, -h_st)
    .lineTo(a + t_w, 0.0)
    .spline(outer[1:], tangents=[(0, 1), (-1, 0)], includeCurrent=True)
    .lineTo(0.0, b)
    .spline(inner_rev[1:], tangents=[(1, 0), (0, -1)], includeCurrent=True)
    .lineTo(a, -h_st)
    .close()
)
shell = prof.revolve(360, (0, 0, 0), (0, 1, 0))

# Nozzle / flange for pressure gauge
nozzle_top = b + t_w + 30.0
nozzle = (
    cq.Workplane("XZ", origin=(0, b, 0))
    .circle(20.0)
    .extrude(-(nozzle_top - b))
)
shell = shell.union(nozzle)

bore = (
    cq.Workplane("XZ", origin=(0, b - 15, 0))
    .circle(15.0)
    .extrude(-(nozzle_top - b + 20))
)
shell = shell.cut(bore)

# Orient tank axis along Z
result = shell.rotate((0, 0, 0), (1, 0, 0), 90)
