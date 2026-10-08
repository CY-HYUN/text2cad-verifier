import cadquery as cq

# 60 x 60 base, 100 tall (Y = front-to-back direction, front at Y=-30)
box = cq.Workplane("XY").box(60, 60, 100, centered=(True, True, False))

# Triangular cutting tool in the side profile (YZ plane):
# from front edge at Z=60 up to back edge at Z=100
cutter = (
    cq.Workplane("YZ")
    .polyline([(-30, 60), (30, 100), (30, 130), (-30, 130)])
    .close()
    .extrude(40, both=True)
)
body = box.cut(cutter)

# Shell, removing the bottom face, 5 mm wall
body = body.faces("<Z").shell(-5)

# Ø20 through hole in the higher rear face (Y=+30), centred on that face
hole = cq.Solid.makeCylinder(10, 15, cq.Vector(0, 18, 50), cq.Vector(0, 1, 0))
result = body.cut(cq.Workplane("XY").add(hole))
