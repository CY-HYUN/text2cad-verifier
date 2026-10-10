import cadquery as cq

end_d = 30.0
mid_d = 15.0
seg_len = 20.0

bottom = cq.Workplane("XY").circle(end_d / 2).extrude(seg_len)
middle = cq.Workplane("XY").workplane(offset=seg_len).circle(mid_d / 2).extrude(seg_len)
top = cq.Workplane("XY").workplane(offset=2 * seg_len).circle(end_d / 2).extrude(seg_len)

result = bottom.union(middle).union(top)
