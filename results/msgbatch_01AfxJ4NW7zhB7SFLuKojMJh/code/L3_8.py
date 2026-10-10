import cadquery as cq
import math

T = 3.0
# Converging section: cubic Bezier (axis along X, y = radius)
P0 = (0.0, 25.0); P1 = (15.0, 25.0); P2 = (15.0, 10.0); P3 = (30.0, 10.0)

def bez(t):
    u = 1 - t
    x = u**3*P0[0] + 3*u*u*t*P1[0] + 3*u*t*t*P2[0] + t**3*P3[0]
    y = u**3*P0[1] + 3*u*u*t*P1[1] + 3*u*t*t*P2[1] + t**3*P3[1]
    dx = 3*u*u*(P1[0]-P0[0]) + 6*u*t*(P2[0]-P1[0]) + 3*t*t*(P3[0]-P2[0])
    dy = 3*u*u*(P1[1]-P0[1]) + 6*u*t*(P2[1]-P1[1]) + 3*t*t*(P3[1]-P2[1])
    return x, y, dx, dy

a = 20.0 / 50.0**2  # parabola with vertex at throat, reaching r=30 at x=80

def par(x):
    s = x - 30.0
    return x, 10.0 + a*s*s, 1.0, 2*a*s

samples = []
N1 = 30
for i in range(N1 + 1):
    samples.append(bez(i / N1))
N2 = 30
for i in range(1, N2 + 1):
    samples.append(par(30.0 + 50.0 * i / N2))

inner = []
outer = []
for x, y, dx, dy in samples:
    L = math.hypot(dx, dy)
    nx, ny = -dy / L, dx / L
    inner.append((x, y))
    outer.append((x + T*nx, y + T*ny))

# fix end positions exactly (tangent horizontal there)
outer[0] = (0.0, 25.0 + T)
outer[-1] = (80.0, outer[-1][1])

w = (cq.Workplane("XY")
     .moveTo(*inner[0])
     .spline(inner[1:], includeCurrent=True)
     .lineTo(*outer[-1])
     .spline(outer[::-1][1:], includeCurrent=True)
     .close())

result = w.revolve(360, (0, 0, 0), (1, 0, 0))
