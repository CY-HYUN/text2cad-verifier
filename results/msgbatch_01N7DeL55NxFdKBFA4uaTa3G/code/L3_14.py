import cadquery as cq
import math

# Base plate: 100 x 50, 5 mm thick
L, W, T = 100.0, 50.0, 5.0
base = cq.Workplane("XY").box(L, W, T, centered=False)

# Fin parameters
H = 30.0          # fin height
t = 1.0           # wall thickness (symmetric)
amp = 2.0
k = 0.2 * math.pi
y0 = 5.0          # offset from base edge
N = 400

def fin_solid(yoff):
    upper, lower = [], []
    for i in range(N + 1):
        x = L * i / N
        y = yoff + amp * math.sin(k * x)
        dy = amp * k * math.cos(k * x)
        n = math.hypot(1.0, dy)
        nx, ny = -dy / n, 1.0 / n
        upper.append((x + nx * t / 2, y + ny * t / 2))
        lower.append((x - nx * t / 2, y - ny * t / 2))
    pts = upper + lower[::-1]
    fin = (cq.Workplane("XY").workplane(offset=T)
           .polyline(pts).close().extrude(H))
    # trim to base footprint in X
    clip = cq.Workplane("XY").box(L, W + 20, H, centered=False).translate((0, -10, T))
    return fin.intersect(clip)

result = base
for i in range(5):
    result = result.union(fin_solid(y0 + 10.0 * i))
