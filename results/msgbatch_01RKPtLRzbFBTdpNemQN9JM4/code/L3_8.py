import cadquery as cq
import math

# Inner wall profile (x along axis, y = radius)
P0 = (0.0, 25.0)
P1 = (15.0, 25.0)
P2 = (15.0, 10.0)
P3 = (30.0, 10.0)

def bez(t):
    u = 1 - t
    x = u**3*P0[0] + 3*u*u*t*P1[0] + 3*u*t*t*P2[0] + t**3*P3[0]
    y = u**3*P0[1] + 3*u*u*t*P1[1] + 3*u*t*t*P2[1] + t**3*P3[1]
    dx = 3*u*u*(P1[0]-P0[0]) + 6*u*t*(P2[0]-P1[0]) + 3*t*t*(P3[0]-P2[0])
    dy = 3*u*u*(P1[1]-P0[1]) + 6*u*t*(P2[1]-P1[1]) + 3*t*t*(P3[1]-P2[1])
    return x, y, dx, dy

pts = []  # (x, y, dx, dy)
N1 = 30
for i in range(N1):
    pts.append(bez(i / N1))

# Diverging section: parabolic profile with vertex at throat, opening to exit
c = 20.0 / 50.0**2
N2 = 40
for i in range(N2 + 1):
    s = 50.0 * i / N2
    pts.append((30.0 + s, 10.0 + c*s*s, 1.0, 2*c*s))

t_wall = 3.0
inner = []
outer = []
for x, y, dx, dy in pts:
    L = math.hypot(dx, dy)
    nx, ny = -dy / L, dx / L  # outward (away from axis)
    inner.append((x, y))
    outer.append((x + t_wall*nx, y + t_wall*ny))

wp = (cq.Workplane("XY")
      .moveTo(*inner[0])
      .spline(inner[1:], includeCurrent=True)
      .lineTo(*outer[-1])
      .spline(list(reversed(outer))[1:], includeCurrent=True)
      .close())

result = wp.revolve(360, (0, 0, 0), (1, 0, 0))
