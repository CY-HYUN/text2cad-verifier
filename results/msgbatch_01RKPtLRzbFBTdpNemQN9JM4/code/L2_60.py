import cadquery as cq
import math

H = 25.0
ro = 45.0
ri = 20.0

# base ring, axis along Z, from z=0 to z=H
ring = cq.Workplane("XY").circle(ro).circle(ri).extrude(H)

# radial through holes at 0, 60, 120... degrees, at mid-height
for i in range(6):
    ang = i * 60.0
    cyl = (
        cq.Workplane("XY")
        .circle(5.0)
        .extrude(ro + 5.0)
        .rotate((0, 0, 0), (1, 0, 0), -90)  # extrude along +Y -> now along +Y
        .rotate((0, 0, 0), (0, 0, 1), -90)  # turn to +X
        .translate((0, 0, H / 2.0))
        .rotate((0, 0, 0), (0, 0, 1), ang)
    )
    ring = ring.cut(cyl)

# axial countersunk holes on top face at 30, 90, 150... degrees on dia 65 circle
pcr = 32.5
pts = [
    (pcr * math.cos(math.radians(30 + 60 * i)), pcr * math.sin(math.radians(30 + 60 * i)))
    for i in range(6)
]
ring = (
    ring.faces(">Z").workplane(origin=(0, 0, H))
    .pushPoints(pts)
    .cskHole(8.0, 14.0, 90)
)

result = ring
