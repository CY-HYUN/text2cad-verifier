import cadquery as cq

# Frustum via loft: 60x60 square at z=0 to 40x40 square at z=30
frustum = (
    cq.Workplane("XY")
    .rect(60.0, 60.0)
    .workplane(offset=30.0)
    .rect(40.0, 40.0)
    .loft(combine=True)
)

# Central through hole, diameter 20
hole = (
    cq.Workplane("XY")
    .workplane(offset=-1.0)
    .circle(10.0)
    .extrude(32.0)
)

result = frustum.cut(hole)
