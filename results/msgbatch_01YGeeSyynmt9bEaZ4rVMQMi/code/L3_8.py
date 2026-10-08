import cadquery as cq
import math

# ---------------- Inner wall definition ----------------
# Converging section: cubic Bezier from inlet (-30,25) to throat (0,10)
P0 = (-30.0, 25.0)
P1 = (-20.0, 19.0)   # inlet tangent slightly inward
P2 = (-12.0, 10.0)   # horizontal tangent at throat
P3 = (0.0, 10.0)

def bez(t):
    mt = 1 - t
    x = mt**3*P0[0] + 3*mt**2*t*P1[0] + 3*mt*t**2*P2[0] + t**3*P3[0]
    y = mt**3*P0[1] + 3*mt**2*t*P1[1] + 3*mt*t**2*P2[1] + t**3*P3[1]
    return (x, y)

def bez_d(t):
    mt = 1 - t
    dx = 3*mt**2*(P1[0]-P0[0]) + 6*mt*t*(P2[0]-P1[0]) + 3*t**2*(P3[0]-P2[0])
    dy = 3*mt**2*(P1[1]-P0[1]) + 6*mt*t*(P2[1]-P1[1]) + 3*t**2*(P3[1]-P2[1])
    return (dx, dy)

# Diverging section: parabola with vertex at throat through outlet (50,30)
c = (30.0 - 10.0) / 50.0**2
def par(x):
    return (x, 10.0 + c*x*x)
def par_d(x):
    return (1.0, 2*c*x)

inner = []
tangents = []
N1 = 16
for i in range(N1 + 1):
    t = i / N1
    inner.append(bez(t))
    tangents.append(bez_d(t))
N2 = 20
for i in range(1, N2 + 1):
    x = 50.0 * i / N2
    inner.append(par(x))
    tangents.append(par_d(x))

# ---------------- Offset outward by 3 mm ----------------
wall = 3.0
outer = []
for (x, y), (dx, dy) in zip(inner, tangents):
    L = math.hypot(dx, dy)
    nx, ny = -dy / L, dx / L   # left normal of +x traversal -> outward
    outer.append((x + wall*nx, y + wall*ny))

outer_rev = list(reversed(outer))

# ---------------- Closed profile ----------------
profile = (
    cq.Workplane("XY")
    .moveTo(*inner[0])
    .spline(inner[1:], includeCurrent=True)
    .lineTo(*outer_rev[0])
    .spline(outer_rev[1:], includeCurrent=True)
    .close()
)

# ---------------- Revolve about X axis ----------------
result = profile.revolve(360, (0, 0, 0), (1, 0, 0))
