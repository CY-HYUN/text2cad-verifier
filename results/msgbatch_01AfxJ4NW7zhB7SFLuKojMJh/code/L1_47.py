import cadquery as cq

# Shaft: diameter 40, length 80, axis along Z
shaft = cq.Workplane("XY").circle(20).extrude(80)

# Keyway: track-shaped slot, 40 long (along Z), 10 wide, 5 deep from the surface (x = 20 -> 15)
slot = (
    cq.Workplane("YZ")
    .workplane(offset=15)
    .center(0, 40)
    .slot2D(40, 10, 90)
    .extrude(10)
)

result = shaft.cut(slot)
