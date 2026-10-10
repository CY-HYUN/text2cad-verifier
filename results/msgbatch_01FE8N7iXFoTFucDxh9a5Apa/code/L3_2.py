import cadquery as cq
import math

# Parameters
L = 100.0      # length (X)
W = 50.0       # width (Z)
T_base = 3.0   # base thickness
A = 5.0        # amplitude
lam = 20.0     # wavelength
off = 5.0      # vertical offset
t = 1.0        # fin wall thickness

# Base: top surface at Y=0
base = (cq.Workplane("XY")
        .box(L, T_base, W, centered=False)
        .translate((0, -T_base, 0)))

# Fin profile: offset sine centerline by +/- t/2 along normal
N = 500
upper = []
lower = []
k = 2 * math.pi / lam
for i in range(N + 1):
    x = L * i / N
    y = A * math.sin(k * x) + off
    dy = A * k * math.cos(k * x)
    n = math.hypot(dy, 1.0)
    nx, ny = -dy / n, 1.0 / n
    upper.append((x + 0.5 * t * nx, y + 0.5 * t * ny))
    lower.append((x - 0.5 * t * nx, y - 0.5 * t * ny))

pts = upper + lower[::-1]

fin = (cq.Workplane("XY")
       .polyline(pts).close()
       .extrude(W))

# Trim fin to the base footprint in X
trim = cq.Workplane("XY").box(L, 20, W, centered=False).translate((0, -5, 0))
fin = fin.intersect(trim)

result = base.union(fin)
