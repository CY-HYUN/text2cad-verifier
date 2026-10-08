import cadquery as cq

# Lower cuboid
base = cq.Workplane("XY").rect(100.0, 60.0).extrude(20.0)

# Upper centered block on top face
upper = (
    cq.Workplane("XY")
    .workplane(offset=20.0)
    .rect(100.0, 30.0)
    .extrude(20.0)
)

result = base.union(upper)
