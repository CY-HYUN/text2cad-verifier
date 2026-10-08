import cadquery as cq

# Sphere of radius 40 mm centered at the origin
sphere = cq.Workplane("XY").sphere(40)

# Through-all cut along Z: 30 mm diameter circle at (25, 0) on the XY plane
cutter = (
    cq.Workplane("XY")
    .workplane(offset=-100)
    .center(25, 0)
    .circle(15)
    .extrude(200)
)

result = sphere.cut(cutter)
