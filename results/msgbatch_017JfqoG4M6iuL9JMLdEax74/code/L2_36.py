import cadquery as cq
import math

outer_d = 120.0
inner_d = 80.0
thk = 20.0
pcd = 100.0
cb_d = 10.0
cb_depth = 10.0
thru_d = 6.0

ring = (
    cq.Workplane("XY")
    .circle(outer_d / 2)
    .circle(inner_d / 2)
    .extrude(thk)
)

pts = [
    (pcd / 2 * math.cos(math.radians(60 * i)), pcd / 2 * math.sin(math.radians(60 * i)))
    for i in range(6)
]

result = (
    ring.faces(">Z").workplane()
    .pushPoints(pts)
    .cboreHole(thru_d, cb_d, cb_depth)
)
