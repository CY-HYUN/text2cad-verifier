import cadquery as cq

base = cq.Workplane("XY").rect(40, 40).extrude(20.0)
result = base.faces(">Z").workplane().center(0, 0).circle(10.0).extrude(20.0)
