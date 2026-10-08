import cadquery as cq

outer_d = 40.0
inner_d = 30.0
height = 50.0
brace_w = 3.0

# Outer tube
tube = (
    cq.Workplane("XY")
    .circle(outer_d / 2)
    .circle(inner_d / 2)
    .extrude(height)
)

# Cross brace (extends into tube wall so it fuses solidly)
brace_len = (inner_d + outer_d) / 2  # ends sit inside the wall
brace = (
    cq.Workplane("XY")
    .rect(brace_len, brace_w)
    .extrude(height)
    .union(cq.Workplane("XY").rect(brace_w, brace_len).extrude(height))
)

result = tube.union(brace)
