import cadquery as cq

# Outer block: 100 x 50 x 30 mm, base on the XY plane
result = cq.Workplane("XY").box(100.0, 50.0, 30.0, centered=(True, True, False))

# Centered through-length slot (100 x 30 mm), cut 20 mm deep from the top face
slot = (
    cq.Workplane("XY")
    .workplane(offset=30.0 - 20.0)
    .rect(100.0, 30.0)
    .extrude(20.0)
)
result = result.cut(slot)
