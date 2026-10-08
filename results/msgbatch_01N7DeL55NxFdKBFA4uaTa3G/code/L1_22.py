import cadquery as cq

# Square frustum: 60 mm bottom square lofted to 40 mm top square, 30 mm tall
frustum = (
    cq.Workplane("XY")
    .rect(60.0, 60.0)
    .workplane(offset=30.0)
    .rect(40.0, 40.0)
    .loft(combine=True)
)

# Central 20 mm through hole, cut from the top face downward
result = (
    frustum.faces(">Z")
    .workplane()
    .hole(20.0)
)
