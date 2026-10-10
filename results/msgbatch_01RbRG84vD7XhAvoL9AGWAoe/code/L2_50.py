import cadquery as cq

# Stepped shaft along the X axis; left end face at x = 0
left_d, left_l = 40.0, 30.0
mid_d, mid_l = 30.0, 40.0
right_d, right_l = 20.0, 30.0
total_l = left_l + mid_l + right_l

left = cq.Workplane("YZ").circle(left_d / 2).extrude(left_l)
mid = (
    cq.Workplane("YZ")
    .workplane(offset=left_l)
    .circle(mid_d / 2)
    .extrude(mid_l)
)
right = (
    cq.Workplane("YZ")
    .workplane(offset=left_l + mid_l)
    .circle(right_d / 2)
    .extrude(right_l)
)
shaft = left.union(mid).union(right)

# Flat-bottomed keyway on top of the middle section (rounded ends)
key_len, key_w, key_depth = 20.0, 6.0, 3.5
key_cx = left_l + mid_l / 2
top_z = mid_d / 2
key = (
    cq.Workplane("XY")
    .workplane(offset=top_z - key_depth)
    .center(key_cx, 0)
    .slot2D(key_len, key_w, 0)
    .extrude(key_depth + 1.0)
)
shaft = shaft.cut(key)

# Center holes at both end faces
hole_d, hole_depth = 5.0, 10.0
h1 = cq.Workplane("YZ").circle(hole_d / 2).extrude(hole_depth)
h2 = (
    cq.Workplane("YZ")
    .workplane(offset=total_l - hole_depth)
    .circle(hole_d / 2)
    .extrude(hole_depth)
)
shaft = shaft.cut(h1).cut(h2)

result = shaft
