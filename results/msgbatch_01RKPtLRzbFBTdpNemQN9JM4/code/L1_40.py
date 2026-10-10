import cadquery as cq

# Stepped shaft along the Z axis, built from three coaxial cylinders.
# The description contradicts itself: it says thinner ends, but the stated
# diameters (middle 15 mm, ends 30 mm) and "dumbbell-like" imply thicker ends.
# I followed the stated dimensions.
end_d = 30.0
mid_d = 15.0
seg_len = 20.0

end1 = cq.Workplane("XY").circle(end_d / 2).extrude(seg_len)
mid = cq.Workplane("XY").workplane(offset=seg_len).circle(mid_d / 2).extrude(seg_len)
end2 = cq.Workplane("XY").workplane(offset=2 * seg_len).circle(end_d / 2).extrude(seg_len)

result = end1.union(mid).union(end2)
