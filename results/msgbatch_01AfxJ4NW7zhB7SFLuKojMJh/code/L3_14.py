import cadquery as cq
import math

L, W, T = 100.0, 50.0, 5.0
H = 30.0
th = 1.0
A = 2.0
k = 0.2 * math.pi

base = cq.Workplane("XY").box(L, W, T, centered=(True, True, False))

N = 200
upper = []
lower = []
for i in range(N + 1):
    x = L * i / N
    y = A * math.sin(k * x)
    s = A * k * math.cos(k * x)
    n = math.hypot(s, 1.0)
    nx, ny = -s / n, 1.0 / n
    upper.append((x - L / 2 + nx * th / 2, y + ny * th / 2))
    lower.append((x - L / 2 - nx * th / 2, y - ny * th / 2))

pts = upper + lower[::-1]

result = base
for j in range(-2, 3):
    yc = j * 10.0
    shifted = [(px, py + yc) for px, py in pts]
    fin = (cq.Workplane("XY").workplane(offset=T)
           .polyline(shifted).close().extrude(H))
    result = result.union(fin)
