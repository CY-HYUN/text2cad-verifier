import cadquery as cq

# Base block 60x60x100
box = cq.Workplane("XY").box(60, 60, 100, centered=(True, True, False))

# Triangular cutting profile in the side plane (local x = Y, local y = Z), extruded along X
wedge = (
    cq.Workplane("YZ")
    .polyline([(-30, 60), (30, 100), (-30, 100)])
    .close()
    .extrude(40, both=True)
)
body = box.cut(wedge)

# Shell: remove the bottom face, 5 mm wall
body = body.faces("<Z").shell(-5)

# Hole of diameter 20 on the rear (high) face at Y=+30
hole = (
    cq.Workplane("XZ")
    .workplane(offset=-30)
    .center(0, 50)
    .circle(10)
    .extrude(6)
)
result = body.cut(hole)
