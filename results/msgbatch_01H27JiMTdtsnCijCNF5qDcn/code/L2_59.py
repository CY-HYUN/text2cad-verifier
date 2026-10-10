import cadquery as cq

cube = cq.Workplane("XY").box(50, 50, 50)

# Front face hole (face at -Y), cut 30 deep into the cube
front_hole = (
    cq.Workplane("XZ", origin=(0, -25, 0))
    .circle(7.5)
    .extrude(-30)  # XZ normal is -Y; negative extrude goes toward +Y
)

# Top face hole (face at +Z), cut 30 deep downward
top_hole = (
    cq.Workplane("XY", origin=(0, 0, 25))
    .circle(7.5)
    .extrude(-30)
)

result = cube.cut(front_hole).cut(top_hole)
