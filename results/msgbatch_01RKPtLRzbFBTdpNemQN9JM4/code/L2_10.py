import cadquery as cq

base = cq.Workplane("XY").box(80, 40, 10, centered=(True, True, False))
left = cq.Workplane("XY").box(10, 40, 40, centered=(True, True, False)).translate((-35, 0, 10))
right = cq.Workplane("XY").box(10, 40, 40, centered=(True, True, False)).translate((35, 0, 10))
result = base.union(left).union(right)

hole_l = cq.Workplane("YZ").workplane(offset=-40).center(0, 30).circle(5).extrude(10)
hole_r = cq.Workplane("YZ").workplane(offset=30).center(0, 30).circle(5).extrude(10)
cs = cq.Workplane("YZ").workplane(offset=38).center(0, 30).circle(10).extrude(2)

result = result.cut(hole_l).cut(hole_r).cut(cs)
