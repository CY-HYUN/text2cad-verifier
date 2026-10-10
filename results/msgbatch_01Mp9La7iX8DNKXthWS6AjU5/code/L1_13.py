import cadquery as cq

# Horizontal cylinder along X, from X=0 to X=80
horiz = cq.Workplane("YZ").circle(10.0).extrude(80.0)

# Vertical cylinder at X=40, extruded 40 mm along +Z from the axis
vert = (cq.Workplane("YZ").workplane(offset=40.0)
        .circle(10.0).extrude(1e-6))  # placeholder datum plane (negligible)
vert = cq.Workplane("XY").center(40.0, 0).circle(10.0).extrude(40.0)

result = horiz.union(vert)
