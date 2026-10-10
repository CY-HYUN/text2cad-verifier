import cadquery as cq
import math

# Converging section: cubic Bezier from inlet to throat (tangent horizontal at throat)
P0 = (-30.0, 25.0)
P1 = (-20.0, 22.0)   # slight inward tangent at inlet
P2 = (-10.0, 10.0)
P3 = (0.0, 10.0)     # horizontal tangent at throat

def bez(t):
    mt = 1 - t
    x = mt**3*P0[0] + 3*mt*mt*t*P1[0] + 3*mt*t*t*P2[0] + t**3*P3[0]
    y = mt**3*P0[1] + 3*mt*mt*t*P1[1] + 3*mt*t*t*P2[1] + t**3*P3[1]
    dx = 3*mt*mt*(P1[0]-P0[0]) + 6*mt*t*(P2[0]-P1[0]) + 3*t*t*(P3[0]-P2[0])
    dy = 3*mt*mt*(P1[1]-P0[1]) + 6*mt*t*(P2[1]-P1[1]) + 3*t*t*(P3[1]-P2[1])
    return x, y, dx, dy

# Diverging section: parabola y = 10 + 0.008 x^2, x in [0, 50]
def par(t):
    x = 50.0*t
    y = 10.0 + 20.0*t*t
    return x, y, 50.0, 40.0*t

N = 12
samples = []
for i in range(N + 1):
    samples.append(bez(i / N))
for i in range(1, N + 1):
    samples.append(par(i / N))

t_off = 3.0
inner = []
outer = []
for x, y, dx, dy in samples:
    L = math.hypot(dx, dy)
    nx, ny = -dy / L, dx / L   # upward (away from axis)
    inner.append((x, y))
    outer.append((x + t_off*nx, y + t_off*ny))

inner_tans = [(10.0, -3.0), (50.0, 40.0)]
outer_tans = [(10.0, -3.0), (50.0, 40.0)]

sk = (
    cq.Workplane("XY")
    .moveTo(*inner[0])
    .spline(inner[1:], tangents=inner_tans, includeCurrent=True)
    .lineTo(*outer[-1])
    .spline(list(reversed(outer))[1:], tangents=[(-50.0, -40.0), (-10.0, 3.0)], includeCurrent=True)
    .close()
)

result = sk.revolve(360, (0, 0, 0), (1, 0, 0))
