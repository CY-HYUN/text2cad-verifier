import cadquery as cq
import math

# Key points (X along axis, Y = radius)
P0 = (-30.0, 25.0)   # inlet
P1 = (-20.0, 20.0)   # inlet handle (slightly inward)
P2 = (-10.0, 10.0)   # throat handle (horizontal tangent)
P3 = (0.0, 10.0)     # throat
outlet = (50.0, 30.0)
wall = 3.0

# Diverging parabola: vertex at throat, y = 10 + c*x^2 through outlet
c = (outlet[1] - P3[1]) / (outlet[0] ** 2)

def bez(t):
    mt = 1 - t
    x = mt**3*P0[0] + 3*mt**2*t*P1[0] + 3*mt*t**2*P2[0] + t**3*P3[0]
    y = mt**3*P0[1] + 3*mt**2*t*P1[1] + 3*mt*t**2*P2[1] + t**3*P3[1]
    dx = 3*mt**2*(P1[0]-P0[0]) + 6*mt*t*(P2[0]-P1[0]) + 3*t**2*(P3[0]-P2[0])
    dy = 3*mt**2*(P1[1]-P0[1]) + 6*mt*t*(P2[1]-P1[1]) + 3*t**2*(P3[1]-P2[1])
    return (x, y), (dx, dy)

def para(x):
    return (x, P3[1] + c*x*x), (1.0, 2*c*x)

samples = []
n1, n2 = 16, 20
for i in range(n1 + 1):
    samples.append(bez(i / n1))
for i in range(1, n2 + 1):
    samples.append(para(outlet[0] * i / n2))

inner, outer = [], []
for (p, d) in samples:
    L = math.hypot(d[0], d[1])
    nx, ny = -d[1] / L, d[0] / L   # outward normal (away from axis)
    inner.append(p)
    outer.append((p[0] + wall*nx, p[1] + wall*ny))

outer_rev = list(reversed(outer))

profile = (
    cq.Workplane("XY")
    .moveTo(*inner[0])
    .spline(inner[1:], includeCurrent=True)
    .lineTo(*outer_rev[0])
    .spline(outer_rev[1:], includeCurrent=True)
    .close()
)

result = profile.revolve(360, (0, 0, 0), (1, 0, 0))
