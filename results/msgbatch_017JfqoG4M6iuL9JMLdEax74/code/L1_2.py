import cadquery as cq

outer_d = 40.0
inner_d = 25.0
length = 120.0

# Hollow cylinder with its axis along X (length direction)
result = (
    cq.Workplane("YZ")
    .circle(outer_d / 2)
    .circle(inner_d / 2)
    .extrude(length)
)
