import cadquery as cq

# Frustum: 60 mm square base, 40 mm square top, 30 mm tall
result = (
    cq.Workplane("XY")
    .rect(60.0, 60.0)
    .workplane(offset=30.0)
    .rect(40.0, 40.0)
    .loft(combine=True)
)

# Central 20 mm through-hole, cut from the top face
result = (
    result.faces(">Z").workplane()
    .circle(10.0)
    .cutThruAll()
)
