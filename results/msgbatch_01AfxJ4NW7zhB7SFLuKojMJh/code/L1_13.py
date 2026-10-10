import cadquery as cq

horiz = cq.Workplane("YZ").circle(10).extrude(40, both=True)
vert = cq.Workplane("XY").circle(10).extrude(40)
result = horiz.union(vert)
