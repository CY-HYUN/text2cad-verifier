import cadquery as cq

base = cq.Workplane("XY").rect(60, 60).workplane(offset=30).rect(40, 40).loft(combine=True)
hole = cq.Workplane("XY").circle(10).extrude(30)
result = base.cut(hole)
