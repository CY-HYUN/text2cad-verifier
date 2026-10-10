import cadquery as cq

r = 10.0
seg1 = cq.Workplane("YZ").circle(r).extrude(50.0)

plane = cq.Plane(origin=(50, 0, 0), xDir=(1, 0, 0), normal=(0, 1, 0))
seg2 = cq.Workplane(plane).circle(r).extrude(50.0)

result = seg1.union(seg2)
