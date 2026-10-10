import cadquery as cq

# Base box 60x60x100
body = cq.Workplane("XY").box(60, 60, 100, centered=(True, True, False))

# Triangular wedge cut on the YZ plane (local x = Y, local y = Z)
wedge = (
    cq.Workplane("YZ")
    .polyline([(-30, 60), (30, 100), (-30, 100)])
    .close()
    .extrude(35, both=True)
)
body = body.cut(wedge)

# Shell: remove bottom face, 5 mm wall
body = body.faces("<Z").shell(-5)

# Circle d=20 on rear face (y=+30), cut through the rear wall
hole = (
    cq.Workplane("XZ", origin=(0, 35, 0))
    .center(0, 50)
    .circle(10)
    .extrude(15)  # XZ normal is -Y: spans y=35 to y=20
)
result = body.cut(hole)
