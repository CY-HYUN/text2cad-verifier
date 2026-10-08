import cadquery as cq
import math

OD, ID, H = 90.0, 40.0, 25.0
radial_d = 10.0
pcd = 65.0
hole_d = 6.6
csk_d = 12.0
csk_depth = (csk_d - hole_d) / 2.0  # 90 deg countersink

# Base ring
ring = cq.Workplane("XY").circle(OD / 2).circle(ID / 2).extrude(H)

# Radial holes (6x), through one wall at Z=12.5
for i in range(6):
    a = math.radians(i * 60)
    d = cq.Vector(math.cos(a), math.sin(a), 0)
    start = cq.Vector(d.x * (ID / 2 - 2), d.y * (ID / 2 - 2), H / 2)
    cyl = cq.Solid.makeCylinder(radial_d / 2, OD / 2 - ID / 2 + 10, start, d)
    ring = ring.cut(cq.Workplane().add(cyl))

# Axial countersunk holes (6x) on PCD 65, starting at 30 deg
for i in range(6):
    a = math.radians(30 + i * 60)
    x, y = pcd / 2 * math.cos(a), pcd / 2 * math.sin(a)
    thru = cq.Solid.makeCylinder(hole_d / 2, H + 2, cq.Vector(x, y, -1), cq.Vector(0, 0, 1))
    cone = cq.Solid.makeCone(csk_d / 2, hole_d / 2, csk_depth,
                             cq.Vector(x, y, H), cq.Vector(0, 0, -1))
    ring = ring.cut(cq.Workplane().add(thru)).cut(cq.Workplane().add(cone))

result = ring
