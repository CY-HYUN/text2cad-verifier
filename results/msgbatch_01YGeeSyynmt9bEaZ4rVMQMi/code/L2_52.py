import cadquery as cq

# Base block 60 x 60 x 100 (X width, Y depth, Z height), bottom at Z=0
box = cq.Workplane("XY").box(60, 60, 100, centered=(True, True, False))

# Triangular cutter: line from front edge (Y=-30, Z=60) to back edge (Y=30, Z=100)
cutter = (
    cq.Workplane("YZ")
    .polyline([(-30, 60), (30, 100), (-30, 100)])
    .close()
    .extrude(40, both=True)
)
body = box.cut(cutter)

# Shell, removing the bottom face, 5 mm wall thickness
shelled = body.faces("<Z").shell(-5)

# Through hole (D20) in the higher rear face (Y=+30), centered on the face
hole = (
    cq.Workplane("XZ", origin=(0, 20, 0))
    .center(0, 50)
    .circle(10)
    .extrude(-20)  # extends toward +Y, through the rear wall
)

result = shelled.cut(hole)
