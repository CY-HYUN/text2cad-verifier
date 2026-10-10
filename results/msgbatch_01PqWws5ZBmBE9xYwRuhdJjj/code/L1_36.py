import cadquery as cq

# Create outer cylinder
outer_cylinder = (
    cq.Workplane("XY")
    .circle(40.0)  # radius = diameter/2 = 80/2 = 40
    .extrude(20.0)
)

# Create inner cylinder (offset by 10mm in +X direction)
inner_cylinder = (
    cq.Workplane("XY")
    .moveTo(10.0, 0)  # offset center by 10mm along +X
    .circle(20.0)  # radius = diameter/2 = 40/2 = 20
    .extrude(20.0)
)

# Perform difference operation to create eccentric ring
result = outer_cylinder.cut(inner_cylinder)
