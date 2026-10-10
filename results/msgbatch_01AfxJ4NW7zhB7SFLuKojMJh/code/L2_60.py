import cadquery as cq
import math

H = 25.0
ro = 45.0
ri = 20.0

# Base ring, axis along Z, from z=0 to z=H
ring = cq.Workplane("XY").circle(ro).circle(ri).extrude(H)

# Radial through-holes (dia 10) at 0, 60, 120... deg, at mid-height
for i in range(6):
    ang = i * 60.0
    cutter = (
        cq.Workplane("XY")
        .circle(5.0)
        .extrude(ro + 5.0)          # along +Z, then rotate to the radial direction
    )
    # Orient cylinder along +X, starting inside the bore
    cutter = (
        cq.Workplane("YZ")
        .workplane(offset=ri - 1.0)
        .center(0, H / 2.0)
        .circle(5.0)
        .extrude(ro - ri + 2.0)
        .rotate((0, 0, 0), (0, 0, 1), ang)
    )
    ring = ring.cut(cutter)

# Axial countersunk holes (dia 8) on 65 mm PCD at 30, 90, ... deg from the top face
pcd_r = 32.5
pts = [
    (pcd_r * math.cos(math.radians(30 + 60 * i)),
     pcd_r * math.sin(math.radians(30 + 60 * i)))
    for i in range(6)
]
ring = (
    ring.faces(">Z").workplane(origin=(0, 0, H))
    .pushPoints(pts)
    .cskHole(8.0, 14.0, 90.0)
)

result = ring
