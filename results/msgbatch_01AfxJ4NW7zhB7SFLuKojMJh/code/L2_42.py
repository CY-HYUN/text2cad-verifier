import cadquery as cq

h = cq.Workplane("XY").box(100, 60, 10, centered=False)
v = cq.Workplane("XY").box(10, 60, 100, centered=False)

# holes
h = h.cut(cq.Workplane("XY").center(50, 30).circle(10).extrude(10))
v = v.cut(cq.Workplane("YZ").center(30, 50).circle(10).extrude(10))

rib = (cq.Workplane("XZ").polyline([(10, 10), (60, 10), (10, 60)]).close()
       .extrude(10).translate((0, 35, 0)))

result = h.union(v).union(rib)
