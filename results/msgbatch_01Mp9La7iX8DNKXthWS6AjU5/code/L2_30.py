import cadquery as cq

box = cq.Workplane("XY").box(60, 30, 30, centered=(True, True, False))

# semi-elliptical arch cut from front, through all depth
ell = (cq.Workplane("XZ").ellipse(20, 15).extrude(50, both=True))
box = box.cut(ell)

# circular hole from top, cut fully downward
hole = cq.Workplane("XY").workplane(offset=30).circle(5).extrude(-30)
result = box.cut(hole)
