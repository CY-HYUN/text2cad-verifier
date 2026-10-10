import cadquery as cq
import math

L = 100.0
W = 50.0
T_base = 5.0
H_fin = 30.0
t_fin = 1.0
A = 2.0
k = 0.2 * math.pi

# Base plate (bottom flat at z=0)
base = cq.Workplane("XY").box(L, W, T_base, centered=(True, True, False))

# Sine fin profile (closed polygon), X from -L/2 to L/2
N = 200
xs = [-L / 2 + L * i / N for i in range(N + 1)]

def fin(yc):
    upper = [(x, yc + A * math.sin(k * (x + L / 2)) + t_fin / 2) for x in xs]
    lower = [(x, yc + A * math.sin(k * (x + L / 2)) - t_fin / 2) for x in reversed(xs)]
    pts = upper + lower
    return (
        cq.Workplane("XY")
        .workplane(offset=T_base)
        .polyline(pts)
        .close()
        .extrude(H_fin)
    )

result = base
for i in range(5):
    yc = -20.0 + 10.0 * i
    result = result.union(fin(yc))
