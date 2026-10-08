import cadquery as cq

beam1 = cq.Workplane("XY").rect(100.0, 20.0).extrude(20.0)
beam2 = cq.Workplane("XY").rect(20.0, 100.0).extrude(20.0)
result = beam1.union(beam2)
