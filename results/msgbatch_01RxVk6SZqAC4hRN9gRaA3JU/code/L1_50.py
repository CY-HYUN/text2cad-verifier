import cadquery as cq

d = 20.0
L = 50.0

# First segment: circle in YZ plane, extruded +X
seg1 = cq.Workplane("YZ").circle(d / 2).extrude(L)

# Second segment: plane parallel to XZ at end face center (50,0,0), extrude +Y
plane2 = cq.Plane(origin=(L, 0, 0), xDir=(1, 0, 0), normal=(0, 1, 0))
seg2 = cq.Workplane(plane2).circle(d / 2).extrude(L)

result = seg1.union(seg2)
