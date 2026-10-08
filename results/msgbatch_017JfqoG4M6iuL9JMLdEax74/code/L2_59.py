import cadquery as cq

L = 50.0
D = 15.0
depth = 30.0

cube = cq.Workplane("XY").box(L, L, L)

# Blind hole along X from the -X face
hole_x = (
    cq.Workplane("YZ", origin=(-L / 2, 0, 0))
    .circle(D / 2)
    .extrude(depth)
)

# Blind hole along Z from the +Z face
hole_z = (
    cq.Workplane("XY", origin=(0, 0, L / 2))
    .circle(D / 2)
    .extrude(-depth)
)

result = cube.cut(hole_x).cut(hole_z)
