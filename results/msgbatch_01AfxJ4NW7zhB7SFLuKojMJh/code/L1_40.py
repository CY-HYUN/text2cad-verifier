import cadquery as cq

# The description contradicts itself: it says the ends are thinner, but gives
# the middle as 15 mm and the ends as 30 mm, and calls the part dumbbell-like.
# I followed the stated dimensions, so the ends are the larger diameter.
# All three cylinders are coaxial along Z, spanning z = 0 to 60.
end1 = cq.Workplane("XY").circle(15).extrude(20)
mid = cq.Workplane("XY").workplane(offset=20).circle(7.5).extrude(20)
end2 = cq.Workplane("XY").workplane(offset=40).circle(15).extrude(20)

result = end1.union(mid).union(end2)
