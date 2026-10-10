import cadquery as cq

disc = cq.Workplane("XY").circle(40).extrude(15)
slot1 = cq.Workplane("XY").workplane(offset=10).rect(90, 10).extrude(5)
slot2 = cq.Workplane("XY").workplane(offset=10).rect(10, 90).extrude(5)
result = disc.cut(slot1).cut(slot2)
