import cadquery as cq

# Outer block: 100 x 50 footprint, extruded 30 upward from the XY plane
result = cq.Workplane("XY").rect(100.0, 50.0).extrude(30.0)

# Centered 100 x 30 slot cut 20 deep from the top face
slot = (
    cq.Workplane("XY")
    .workplane(offset=30.0 - 20.0)
    .rect(100.0, 30.0)
    .extrude(20.0)
)

result = result.cut(slot)
