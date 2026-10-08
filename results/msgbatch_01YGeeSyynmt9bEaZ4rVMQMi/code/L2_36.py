import cadquery as cq
import math

# Ring parameters
OD = 120.0
ID = 80.0
T = 20.0

# Hole parameters
PCD = 100.0
csk_d = 10.0
csk_depth = 10.0
thru_d = 6.0
n_holes = 6

# Base ring
ring = (
    cq.Workplane("XY")
    .circle(OD / 2)
    .circle(ID / 2)
    .extrude(T)
)

# Build the cutting tool for a single hole (revolved-cut equivalent)
def hole_tool(x, y):
    # through hole (slightly oversized in length for clean cut)
    thru = cq.Solid.makeCylinder(
        thru_d / 2, T + 2, cq.Vector(x, y, -1), cq.Vector(0, 0, 1)
    )
    # countersink cone: radius thru_d/2 at depth csk_depth, csk_d/2 at top surface
    cone = cq.Solid.makeCone(
        thru_d / 2, csk_d / 2, csk_depth,
        cq.Vector(x, y, T - csk_depth), cq.Vector(0, 0, 1)
    )
    # small cap above top surface to ensure clean cut
    cap = cq.Solid.makeCylinder(
        csk_d / 2, 1.0, cq.Vector(x, y, T), cq.Vector(0, 0, 1)
    )
    return thru.fuse(cone).fuse(cap)

# Circular pattern of 6 holes on the PCD
result = ring
for i in range(n_holes):
    a = 2 * math.pi * i / n_holes
    x = (PCD / 2) * math.cos(a)
    y = (PCD / 2) * math.sin(a)
    result = result.cut(cq.Workplane("XY").add(hole_tool(x, y)))
