import cadquery as cq

# Lower cuboid: 100 x 60 x 20, base on the XY plane
base = cq.Workplane("XY").rect(100.0, 60.0).extrude(20.0)

# Upper block: 100 x 30, centred on the top face, extruded 20 and merged
result = (
    base.faces(">Z").workplane()
    .rect(100.0, 30.0)
    .extrude(20.0)
)
