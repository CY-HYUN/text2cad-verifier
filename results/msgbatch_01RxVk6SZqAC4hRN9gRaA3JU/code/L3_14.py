import cadquery as cq
import math

# Base plate 100 x 50 x 5 (corner at origin)
L, W, T = 100.0, 50.0, 5.0
base = cq.Workplane("XY").box(L, W, T, centered=False)

# Fin parameters
fin_h = 30.0
thk = 1.0
amp = 2.0
k = 0.2 * math.pi
y0 = 5.0
n_fins = 5
spacing = 10.0

def fin_solid(yoff):
    N = 400
    upper, lower = [], []
    for i in range(N + 1):
        x = L * i / N
        y = yoff + amp * math.sin(k * x)
        dy = amp * k * math.cos(k * x)
        n = math.hypot(dy, 1.0)
        nx, ny = -dy / n, 1.0 / n
        upper.append((x + nx * thk / 2, y + ny * thk / 2))
        lower.append((x - nx * thk / 2, y - ny * thk / 2))
    pts = upper + lower[::-1]
    fin = (cq.Workplane("XY").workplane(offset=T)
           .polyline(pts).close().extrude(fin_h))
    # trim to base footprint in X
    clip = cq.Workplane("XY").box(L, W, T + fin_h + 1, centered=False)
    return fin.intersect(clip)

result = base
for i in range(n_fins):
    result = result.union(fin_solid(y0 + i * spacing))
