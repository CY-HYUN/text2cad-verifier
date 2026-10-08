import cadquery as cq

outer_d = 40.0
inner_d = 30.0
length = 50.0
web_t = 2.0

# Tube shell
tube = (
    cq.Workplane("XY")
    .circle(outer_d / 2)
    .circle(inner_d / 2)
    .extrude(length)
)

# Cross web spanning the inner diameter (overlaps slightly into the wall for a clean union)
web_len = inner_d + 1.0
web1 = cq.Workplane("XY").rect(web_len, web_t).extrude(length)
web2 = cq.Workplane("XY").rect(web_t, web_len).extrude(length)

result = tube.union(web1).union(web2)
