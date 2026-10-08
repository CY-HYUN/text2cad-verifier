import cadquery as cq

base = cq.Workplane("XY").rect(40, 40).extrude(20)
result = base.faces(">Z").workplane().center(0, 0).circle(10).extrude(20)
