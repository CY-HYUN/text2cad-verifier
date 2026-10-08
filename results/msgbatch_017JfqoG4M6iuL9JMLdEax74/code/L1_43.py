import cadquery as cq

length = 100.0  # X
width = 50.0    # Y
height = 30.0   # Z

groove_w = 30.0
groove_h = 20.0

body = cq.Workplane("XY").box(length, width, height, centered=(True, True, False))
groove = (
    cq.Workplane("XY")
    .box(length + 2, groove_w, groove_h + 1, centered=(True, True, False))
    .translate((0, 0, height - groove_h))
)
result = body.cut(groove)
