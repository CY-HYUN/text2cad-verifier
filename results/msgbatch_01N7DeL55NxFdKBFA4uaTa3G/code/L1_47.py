import cadquery as cq

# Shaft: Ø40 x 80 along Z
shaft = cq.Workplane("XY").circle(20.0).extrude(80.0)

# Keyway: 10 wide (X) x 80 long (Z), cut 5 deep from y=+20 toward -Y
keyway = (
    cq.Workplane("XY")
    .box(10.0, 5.0 + 1.0, 80.0, centered=(True, False, False))
    .translate((0, 15.0, 0))
)

result = shaft.cut(keyway)
