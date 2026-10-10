import cadquery as cq

result = cq.Workplane("XY").circle(50).circle(25).extrude(5)
