import cadquery as cq

# Sphere of radius 40 mm centered at the origin
sphere = cq.Workplane("XY").sphere(40)

# Through-all cut: 30 mm diameter circle at X=25, Y=0, extruded both ways along Z
cutter = (
    cq.Workplane("XY")
    .workplane(offset=-100)
    .center(25, 0)
    .circle(15)
    .extrude(200)
)

result = sphere.cut(cutter)
