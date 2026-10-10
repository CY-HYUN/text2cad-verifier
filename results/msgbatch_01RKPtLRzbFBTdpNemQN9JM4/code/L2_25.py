import cadquery as cq

# three plates
p1 = cq.Workplane("XY").box(50, 50, 5, centered=False)
p2 = cq.Workplane("XY").box(50, 5, 50, centered=False)
p3 = cq.Workplane("XY").box(5, 50, 50, centered=False)
body = p1.union(p2).union(p3)

# ribs
tri = [(5, 5), (25, 5), (5, 25)]
r1 = cq.Workplane("YZ", origin=(5, 0, 0)).polyline(tri).close().extrude(5)
r2 = cq.Workplane("XZ", origin=(0, 5, 0)).polyline(tri).close().extrude(-5)
r3 = cq.Workplane("XY", origin=(0, 0, 5)).polyline(tri).close().extrude(5)
body = body.union(r1).union(r2).union(r3)

# holes
h1 = cq.Workplane("XY").center(25, 25).circle(7.5).extrude(5)
h2 = cq.Workplane("XZ").center(25, 25).circle(7.5).extrude(-5)
h3 = cq.Workplane("YZ").center(25, 25).circle(7.5).extrude(5)
body = body.cut(h1).cut(h2).cut(h3)

result = body
