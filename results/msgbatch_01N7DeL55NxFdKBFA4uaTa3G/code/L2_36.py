import cadquery as cq
import math

OD = 120.0
ID = 80.0
T = 20.0
PCD = 100.0
CSK_D = 10.0
CSK_DEPTH = 10.0
THRU_D = 6.0
N = 6

# Ring
ring = (
    cq.Workplane("XY")
    .circle(OD / 2)
    .circle(ID / 2)
    .extrude(T)
)

# Build one hole tool (through hole + countersink cone) via revolve-like solids
def hole_tool(x, y):
    thru = cq.Solid.makeCylinder(THRU_D / 2, T + 2, cq.Vector(x, y, -1), cq.Vector(0, 0, 1))
    # cone: small radius at bottom of countersink, large at top surface
    cone = cq.Solid.makeCone(
        THRU_D / 2, CSK_D / 2, CSK_DEPTH,
        cq.Vector(x, y, T - CSK_DEPTH), cq.Vector(0, 0, 1)
    )
    # small cap above top face to ensure clean cut
    cap = cq.Solid.makeCylinder(CSK_D / 2, 1.0, cq.Vector(x, y, T), cq.Vector(0, 0, 1))
    return thru.fuse(cone).fuse(cap)

result = ring
for i in range(N):
    a = 2 * math.pi * i / N
    x = (PCD / 2) * math.cos(a)
    y = (PCD / 2) * math.sin(a)
    result = result.cut(cq.Workplane("XY").add(hole_tool(x, y)))
