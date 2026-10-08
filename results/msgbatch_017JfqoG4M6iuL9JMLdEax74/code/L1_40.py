import cadquery as cq

# Dumbbell-like stepped shaft along Z
end_d = 30.0
end_l = 20.0
mid_d = 15.0
mid_l = 20.0

bottom = cq.Workplane("XY").circle(end_d / 2).extrude(end_l)
middle = cq.Workplane("XY").workplane(offset=end_l).circle(mid_d / 2).extrude(mid_l)
top = cq.Workplane("XY").workplane(offset=end_l + mid_l).circle(end_d / 2).extrude(end_l)

result = bottom.union(middle).union(top)
