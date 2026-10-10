import cadquery as cq

base = cq.Workplane("XY").box(80, 40, 10, centered=(True, True, False))
left = cq.Workplane("XY").box(10, 40, 40, centered=(False, True, False)).translate((-40, 0, 10))
right = cq.Workplane("XY").box(10, 40, 40, centered=(False, True, False)).translate((30, 0, 10))
body = base.union(left).union(right)

# through holes along X
hole = cq.Workplane("YZ").workplane(offset=-50).center(0, 30).circle(5).extrude(100)
body = body.cut(hole)

# countersink / counterbore on right flange outer face
cs = cq.Workplane("YZ").workplane(offset=38).center(0, 30).circle(10).extrude(2)
body = body.cut(cs)

result = body
