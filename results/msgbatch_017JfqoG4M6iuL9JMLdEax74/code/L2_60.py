import cadquery as cq
import math

OD, ID, T = 90.0, 40.0, 25.0
radial_d = 10.0
cs_d = 8.0
cs_head_d = 14.0
cs_angle = 90.0
pcd = 65.0

# Base ring
result = (
    cq.Workplane("XY")
    .circle(OD / 2)
    .circle(ID / 2)
    .extrude(T)
)

# Radial through-holes at 0, 60, 120... degrees (mid-thickness)
for i in range(6):
    ang = math.radians(i * 60)
    d = (math.cos(ang), math.sin(ang), 0)
    cyl = cq.Solid.makeCylinder(
        radial_d / 2,
        OD / 2 + 5,
        cq.Vector(0, 0, T / 2),
        cq.Vector(*d),
    )
    result = result.cut(cq.Workplane("XY").add(cyl))

# Axial countersunk holes at 30, 90, 150... degrees on PCD 65
pts = [
    (pcd / 2 * math.cos(math.radians(30 + i * 60)),
     pcd / 2 * math.sin(math.radians(30 + i * 60)))
    for i in range(6)
]
result = (
    result.faces(">Z").workplane(origin=(0, 0, T))
    .pushPoints(pts)
    .cskHole(cs_d, cs_head_d, cs_angle)
)
