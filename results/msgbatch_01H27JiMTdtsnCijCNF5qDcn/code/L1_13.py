import cadquery as cq

# Horizontal cylinder along X from 0 to 80
cyl1 = cq.Workplane("YZ").circle(10).extrude(80)

# Vertical cylinder at X=40, extruded along +Z by 40
cyl2 = cq.Workplane("XY").center(40, 0).circle(10).extrude(40)

result = cyl1.union(cyl2)
