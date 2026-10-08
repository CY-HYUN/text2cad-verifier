import cadquery as cq

size = 50.0
d = 15.0
depth = 30.0

# 50 mm cube centred at the origin
cube = cq.Workplane("XY").box(size, size, size)

# Hole from the front face (-Y), 30 mm deep along +Y
front_hole = (
    cq.Workplane("XZ", origin=(0, -size / 2, 0))
    .circle(d / 2)
    .extrude(-depth)  # XZ normal is -Y, so negative extrude goes +Y
)

# Hole from the top face (+Z), 30 mm deep along -Z
top_hole = (
    cq.Workplane("XY", origin=(0, 0, size / 2))
    .circle(d / 2)
    .extrude(-depth)
)

result = cube.cut(front_hole).cut(top_hole)
