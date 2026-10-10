import cadquery as cq
import math

# Converging section: cubic Bezier from inlet (-30,25) to throat (0,10)
P0 = (-30.0, 25.0)
P1 = (-20.0, 22.0)   # slightly inward tangent at inlet
P2 = (-10.0, 10.0)   # horizontal tangent at throat
P3 = (0.0, 10.0)

def bez(t):
    u = 1 - t
    x = u**3*P0[0] + 3*u*u*t*P1[0] + 3*u*t*t*P2[0] + t**3*P3[0]
    y = u**3*P0[1] + 3*u*u*t*P1[1] + 3*u*t*t*P2[1] + t**3*P3[1]
    dx = 3*(u*u*(P1[0]-P0[0]) + 2*u*t*(P2[0]-P1[0]) + t*t*(P3[0]-P2[0]))
    dy = 3*(u*u*(P1[1]-P0[1]) + 2*u*t*(P2[1]-P1[1]) + t*t*(P3[1]-P2[1]))
    return (x, y), (dx, dy)

# Diverging section: parabola y = 10 + a x^2 through (50,30)
a = 20.0 / 2500.0
def par(x):
    return (x, 10 + a*x*x), (1.0, 2*a*x)

T = 3.0
def offs(p, d):
    n = math.hypot(d[0], d[1])
    return (p[0] - d[1]/n*T, p[1] + d[0]/n*T)

N = 16
in1, out1, in2, out2 = [], [], [], []
for i in range(N + 1):
    p, d = bez(i / N)
    in1.append(p)
    out1.append(offs(p, d))
for i in range(N + 1):
    p, d = par(50.0 * i / N)
    in2.append(p)
    out2.append(offs(p, d))

w = (cq.Workplane("XZ")
     .moveTo(*in1[0])
     .spline(in1[1:], includeCurrent=True)
     .spline(in2[1:], includeCurrent=True)
     .lineTo(*out2[-1])
     .spline(out2[::-1][1:], includeCurrent=True)
     .spline(out1[::-1][1:], includeCurrent=True)
     .close())

result = w.revolve(360, (0, 0, 0), (1, 0, 0))
