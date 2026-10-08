import cadquery as cq
import math

# Base ring
OD, ID, H = 90.0, 40.0, 25.0
ring = cq.Workplane("XY").circle(OD / 2).circle(ID / 2).extrude(H)

# Radial holes: dia 10 at Z=12.5, through one wall, patterned 6x
for i in range(6):
    ang = i * 60.0
    cyl = (
        cq.Workplane("YZ")
        .workplane(offset=ID / 2 - 5)   # start inside bore
        .center(0, H / 2)
        .circle(5.0)
        .extrude(OD / 2 - ID / 2 + 10)  # through outer wall
        .rotate((0, 0, 0), (0, 0, 1), ang)
    )
    ring = ring.cut(cyl)

# Axial countersunk holes on 65 mm PCD, starting at 30 deg, patterned 6x
pcd_r = 65.0 / 2
pts = [
    (pcd_r * math.cos(math.radians(30 + 60 * i)),
     pcd_r * math.sin(math.radians(30 + 60 * i)))
    for i in range(6)
]
ring = (
    ring.faces(">Z")
    .workplane(origin=(0, 0, H))
    .pushPoints(pts)
    .cskHole(6.6, 12.0, 90)
)

result = ring
