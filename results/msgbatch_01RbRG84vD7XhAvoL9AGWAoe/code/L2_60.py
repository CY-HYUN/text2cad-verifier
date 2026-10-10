import cadquery as cq
import math

OD = 90.0
ID = 40.0
T = 25.0

# Main ring
ring = (
    cq.Workplane("XY")
    .circle(OD / 2)
    .circle(ID / 2)
    .extrude(T)
)

# Radial through holes, d10, at 0, 60, 120 ... deg, mid-thickness
for i in range(6):
    a = i * 60.0
    cyl = (
        cq.Workplane("XY")
        .cylinder(OD, 5.0, direct=cq.Vector(1, 0, 0), centered=(False, True, True))
        .translate((0, 0, T / 2))
        .rotate((0, 0, 0), (0, 0, 1), a)
    )
    ring = ring.cut(cyl)

# Axial countersunk holes, d8, on PCD 65, at 30, 90, 150 ... deg
r = 65.0 / 2
pts = [
    (r * math.cos(math.radians(30 + 60 * i)), r * math.sin(math.radians(30 + 60 * i)))
    for i in range(6)
]
ring = (
    ring.faces(">Z").workplane()
    .pushPoints(pts)
    .cskHole(8.0, 14.0, 90)
)

result = ring
