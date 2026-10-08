import cadquery as cq
import math

D = 30.0
H = 50.0
ang = math.radians(30)
r = D / 2

# Base cylinder (taller than needed, then trimmed)
cyl = cq.Workplane("XY").circle(r).extrude(H + 20)

# Cutting plane: z = H - tan(30)*(x + r)  -> max height H at x=-r
def zc(x):
    return H - math.tan(ang) * (x + r)

x0, x1 = -r - 10, r + 10
cutter = (
    cq.Workplane("XZ")
    .polyline([(x0, zc(x0)), (x1, zc(x1)), (x1, H + 100), (x0, H + 100)])
    .close()
    .extrude(r + 10, both=True)
)

result = cyl.cut(cutter)
