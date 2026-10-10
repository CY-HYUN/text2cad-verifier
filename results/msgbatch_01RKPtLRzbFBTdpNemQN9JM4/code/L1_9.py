import cadquery as cq

handle = cq.Workplane("XY").circle(15).extrude(100)
ball = cq.Workplane("XY").sphere(20).translate((0, 0, 115))
result = handle.union(ball)
