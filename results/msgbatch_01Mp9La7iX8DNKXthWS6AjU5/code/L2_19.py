import cadquery as cq

H = 50
outer = cq.Workplane("XY").circle(20).extrude(H)
inner = cq.Workplane("XY").circle(15).extrude(H)
tube = outer.cut(inner)

t = 3
bar1 = cq.Workplane("XY").rect(40, t).extrude(H)
bar2 = cq.Workplane("XY").rect(t, 40).extrude(H)
cross = bar1.union(bar2).intersect(outer)

result = tube.union(cross)
