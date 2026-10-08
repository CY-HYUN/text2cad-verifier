import cadquery as cq
import math

# Parameters
r_in, r_th, r_ex = 25.0, 10.0, 30.0
L_conv, L_div = 30.0, 50.0
arm = 15.0
t_wall = 3.0

# Converging section: cubic Bezier, tangent parallel to axis at both ends
P0 = (r_in, 0.0)
P1 = (r_in, arm)
P2 = (r_th, L_conv - arm)
P3 = (r_th, L_conv)

def bez(t):
    mt = 1 - t
    r = mt**3*P0[0] + 3*mt**2*t*P1[0] + 3*mt*t**2*P2[0] + t**3*P3[0]
    z = mt**3*P0[1] + 3*mt**2*t*P1[1] + 3*mt*t**2*P2[1] + t**3*P3[1]
    return (r, z)

inner = [bez(i / 20.0) for i in range(21)]

# Diverging section: paraboloid with vertex at throat, opening toward exit
a = (r_ex - r_th) / L_div**2
for i in range(1, 26):
    s = L_div * i / 25.0
    inner.append((r_th + a * s * s, L_conv + s))

# Outer wall: follows the inner wall at constant wall thickness
outer = [(r + t_wall, z) for (r, z) in inner]

wp = (
    cq.Workplane("XZ")
    .moveTo(*inner[0])
    .spline(inner[1:], includeCurrent=True)
    .lineTo(*outer[-1])
    .spline(list(reversed(outer))[1:], includeCurrent=True)
    .close()
)

result = wp.revolve(360, (0, 0, 0), (0, 1, 0))
