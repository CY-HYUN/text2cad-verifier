import cadquery as cq

# Vertical plate: on YZ plane, 40 (Y) x 60 (Z), extruded 10 along +X
vertical = cq.Workplane("YZ").center(20, 30).rect(40, 60).extrude(10)

# Horizontal plate: on XY plane, 50 (X) x 40 (Y), extruded 10 along +Z
horizontal = cq.Workplane("XY").center(25, 20).rect(50, 40).extrude(10)

result = vertical.union(horizontal)
