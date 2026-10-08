import cadquery as cq

outer_d = 40.0
inner_d = 30.0
height = 50.0
brace_w = 3.0
brace_len = (outer_d + inner_d) / 2.0  # extends into the wall for a solid connection

# Outer tube
tube = (
    cq.Workplane("XY")
    .circle(outer_d / 2.0)
    .circle(inner_d / 2.0)
    .extrude(height)
)

# Cross brace
brace_x = cq.Workplane("XY").rect(brace_len, brace_w).extrude(height)
brace_y = cq.Workplane("XY").rect(brace_w, brace_len).extrude(height)

result = tube.union(brace_x).union(brace_y)
