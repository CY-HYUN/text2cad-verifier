import cadquery as cq

body = cq.Workplane("XY").circle(20).extrude(40)

# cone: base radius 15 at z=40, tip at z=25
profile = (cq.Workplane("XZ")
           .moveTo(0, 25)
           .lineTo(15, 40)
           .lineTo(0, 40)
           .close()
           .revolve(360, (0, 0, 0), (0, 1, 0)))

result = body.cut(profile)
