import cadquery as cq

# Base plate
base = cq.Workplane("XY").box(80, 40, 10).translate((0, 0, 5))

# Flanges
left = cq.Workplane("XY").box(10, 40, 40).translate((-35, 0, 30))
right = cq.Workplane("XY").box(10, 40, 40).translate((35, 0, 30))

body = base.union(left).union(right)

# Through holes along X at flange centers (z = 30)
hole = (
    cq.Workplane("YZ")
    .workplane(offset=-50)
    .center(0, 30)
    .circle(5)
    .extrude(100)
)
body = body.cut(hole)

# Counterbore on outer face of right flange: 20 dia, 2 deep
cbore = (
    cq.Workplane("YZ")
    .workplane(offset=38)
    .center(0, 30)
    .circle(10)
    .extrude(2.5)
)
body = body.cut(cbore)

result = body
