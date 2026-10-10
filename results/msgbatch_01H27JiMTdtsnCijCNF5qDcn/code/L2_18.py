import cadquery as cq

# Base block: 100 (X) x 40 (Y) x 30 (Z)
base = cq.Workplane("XY").box(100, 40, 30, centered=(True, True, False))

# Semicircular channel along the full length, centered on the top edge of the end face
cyl = (cq.Workplane("YZ").workplane(offset=-50)
       .center(0, 30).circle(15).extrude(100))
body = base.cut(cyl)

# Side groove on +Y face: 60x10 rectangle, 5 deep, centered on the face
groove = (cq.Workplane("XZ", origin=(0, 20, 15))
          .rect(60, 10).extrude(5))  # XZ normal is -Y, so it cuts inward from y=20
body = body.cut(groove)

# Mirror groove to the -Y side
groove_m = groove.mirror("XZ")
body = body.cut(groove_m)

result = body
