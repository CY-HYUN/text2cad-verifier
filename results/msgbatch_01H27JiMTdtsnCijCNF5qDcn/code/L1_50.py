import cadquery as cq

# First segment: circle in YZ plane, extruded along +X
seg1 = cq.Workplane("YZ").circle(10.0).extrude(50.0)

# Second segment: plane parallel to XZ at the center of the end face (50,0,0), extruded along +Y
# XZ plane normal is -Y, so extrude negative distance to go +Y
seg2 = (
    cq.Workplane("XZ", origin=(50, 0, 0))
    .circle(10.0)
    .extrude(-50.0)
)

result = seg1.union(seg2)
