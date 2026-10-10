import cadquery as cq

# Main shaft: diameter 40, length 80 along Z
shaft = cq.Workplane("XY").circle(20).extrude(80)

# Track-shaped keyway: 40 long (along Z), 10 wide (along Y), 5 deep (from x=20 down to x=15)
key = (
    cq.Workplane("YZ", origin=(15, 0, 0))
    .center(0, 40)
    .slot2D(40, 10, angle=90)
    .extrude(10)
)

result = shaft.cut(key)
