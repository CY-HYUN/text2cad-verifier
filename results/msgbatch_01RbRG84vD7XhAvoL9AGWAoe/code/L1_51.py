import cadquery as cq

R = 30.0
T = 10.0
r_bite = 10.0

disc = cq.Workplane("XY").circle(R).extrude(T)
bite = cq.Workplane("XY").center(R, 0).circle(r_bite).extrude(T)

result = disc.cut(bite)
