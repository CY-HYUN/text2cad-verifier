import cadquery as cq

body = cq.Workplane("XY").box(100, 40, 30)

# semicircular channel along X at top center
cyl = (cq.Workplane("YZ").workplane(offset=-50)
       .center(0, 15).circle(15).extrude(100))
body = body.cut(cyl)

# side groove on +Y face
groove1 = cq.Workplane("XY").box(60, 5, 10).translate((0, 20 - 2.5, 0))
# mirrored groove on -Y face
groove2 = groove1.mirror("XZ")

result = body.cut(groove1).cut(groove2)
