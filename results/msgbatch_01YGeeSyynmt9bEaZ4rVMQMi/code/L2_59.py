import cadquery as cq

size = 50.0
d = 15.0
depth = 30.0

# 50 mm cube centred at origin
result = cq.Workplane("XY").box(size, size, size)

# Front face (-Y) blind hole, 15 mm diameter, 30 mm deep
result = (
    result.faces("<Y")
    .workplane(centerOption="CenterOfBoundBox")
    .hole(d, depth)
)

# Top face (+Z) blind hole, 15 mm diameter, 30 mm deep
result = (
    result.faces(">Z")
    .workplane(centerOption="CenterOfBoundBox")
    .hole(d, depth)
)
