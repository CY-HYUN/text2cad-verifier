import cadquery as cq

# Horizontal cylinder: circle in YZ plane, extruded 80 mm along +X
horiz = cq.Workplane("YZ").circle(10.0).extrude(80.0)

# Vertical branch at X=40, extruded 40 mm along +Z (joined)
vert = cq.Workplane("XY").center(40.0, 0).circle(10.0).extrude(40.0)

result = horiz.union(vert)
