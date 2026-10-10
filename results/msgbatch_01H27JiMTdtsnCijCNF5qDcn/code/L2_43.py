import cadquery as cq

frame = (cq.Workplane("XY").rect(60, 60).extrude(20)
         .faces(">Z").workplane().rect(40, 40).cutThruAll())

cyl = (cq.Workplane("XY").workplane(offset=20).circle(20).extrude(-20))

result = frame.union(cyl)
