import cadquery as cq
import math

L = 100.0      # length (X)
W = 50.0       # width (Y)
T_base = 5.0   # base thickness
H_fin = 30.0   # fin height
t_fin = 1.0    # fin thickness
A = 2.0        # amplitude
k = 0.2 * math.pi  # wave number (period 10 mm)

# Base plate (flat bottom at z=0)
base = cq.Workplane("XY").box(L, W, T_base, centered=(True, True, False))

N = 400
xs = [-L / 2 + L * i / N for i in range(N + 1)]

result = base
for yc in [-20.0, -10.0, 0.0, 10.0, 20.0]:
    top = [(x, yc + A * math.sin(k * x) + t_fin / 2) for x in xs]
    bot = [(x, yc + A * math.sin(k * x) - t_fin / 2) for x in reversed(xs)]
    pts = top + bot
    fin = (
        cq.Workplane("XY")
        .workplane(offset=T_base)
        .polyline(pts)
        .close()
        .extrude(H_fin)
    )
    result = result.union(fin)
