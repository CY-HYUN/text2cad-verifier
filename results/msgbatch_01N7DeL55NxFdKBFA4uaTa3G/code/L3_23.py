import cadquery as cq
import math

# ---------------- Base block ----------------
L, W, H = 200.0, 100.0, 80.0
body = cq.Workplane("XY").box(L, W, H, centered=(True, True, False))

zc = H / 2.0  # center height of oil passages

# ---------------- Internal longitudinal oil passages ----------------
# Main passage (y=0) and two branch galleries (y=±20), drilled from the right end
passages = [
    cq.Solid.makeCylinder(8.0, 180.0, cq.Vector(L / 2, 0, zc), cq.Vector(-1, 0, 0)),
    cq.Solid.makeCylinder(6.0, 180.0, cq.Vector(L / 2, -20, zc), cq.Vector(-1, 0, 0)),
    cq.Solid.makeCylinder(6.0, 180.0, cq.Vector(L / 2, 20, zc), cq.Vector(-1, 0, 0)),
]
for p in passages:
    body = body.cut(cq.Workplane().add(p))

# ---------------- Front oil inlets (XZ face, y=-50) ----------------
for x in (-50.0, 0.0, 50.0):
    inlet = cq.Solid.makeCylinder(10.0, 50.0, cq.Vector(x, -W / 2, zc), cq.Vector(0, 1, 0))
    body = body.cut(cq.Workplane().add(inlet))

# ---------------- Top distribution ports: 2 rows x 5 ----------------
for y in (-20.0, 20.0):
    for x in (-80.0, -40.0, 0.0, 40.0, 80.0):
        port = cq.Solid.makeCylinder(5.0, H - zc, cq.Vector(x, y, H), cq.Vector(0, 0, -1))
        body = body.cut(cq.Workplane().add(port))

# ---------------- Countersunk mounting holes at corners ----------------
corner_pts = [(-90, -40), (90, -40), (-90, 40), (90, 40)]
body = (
    body.faces(">Z").workplane(origin=(0, 0, H))
    .pushPoints(corner_pts)
    .cskHole(9.0, 18.0, 90.0)
)

# ---------------- Lightening pockets ----------------
# Bottom pockets (depth 20, passages bottom at z=32)
bottom_pockets = (
    cq.Workplane("XY")
    .pushPoints([(-50, 0), (50, 0)])
    .slot2D(60.0, 25.0)
    .extrude(20.0)
)
body = body.cut(bottom_pockets)

# Back side pockets (y=+50 face, depth 15 -> y 35..50, galleries end at y=26)
side_pockets = (
    cq.Workplane("XZ", origin=(0, W / 2, 0))
    .pushPoints([(-50, zc), (50, zc)])
    .slot2D(60.0, 20.0)
    .extrude(15.0)
)
body = body.cut(side_pockets)

result = body
