import cadquery as cq
import math

# Parameters
R_in, R_th, R_ex = 25.0, 10.0, 30.0
L_c, L_d = 30.0, 50.0
t = 3.0
arm = 15.0

def bezier(p0, p1, p2, p3, s):
    u = 1 - s
    x = u**3*p0[0] + 3*u*u*s*p1[0] + 3*u*s*s*p2[0] + s**3*p3[0]
    y = u**3*p0[1] + 3*u*u*s*p1[1] + 3*u*s*s*p2[1] + s**3*p3[1]
    return (x, y)

# Converging section: cubic Bezier, tangent to axis direction at both ends
P0 = (0.0, R_in)
P1 = (arm, R_in)
P2 = (L_c - arm, R_th)
P3 = (L_c, R_th)

inner = []
N = 30
for i in range(N + 1):
    inner.append(bezier(P0, P1, P2, P3, i / N))

# Diverging section: paraboloid with vertex at throat, opening toward exit
M = 30
for i in range(1, M + 1):
    s = i / M
    x = L_c + s * L_d
    r = R_th + (R_ex - R_th) * s**2
    inner.append((x, r))

outer = [(x, r + t) for (x, r) in inner]

prof = (
    cq.Workplane("XY")
    .moveTo(*inner[0])
    .spline(inner[1:], includeCurrent=True)
    .lineTo(*outer[-1])
    .spline(list(reversed(outer))[1:], includeCurrent=True)
    .close()
)

result = prof.revolve(360, (0, 0, 0), (1, 0, 0))
