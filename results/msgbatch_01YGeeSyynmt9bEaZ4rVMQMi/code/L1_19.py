import cadquery as cq

# Ring dimensions (mm)
outer_d = 80.0
inner_d = 60.0
height = 20.0

# First ring body: annulus extruded +Z by 20 mm
ring1 = (
    cq.Workplane("XY")
    .circle(outer_d / 2.0)
    .circle(inner_d / 2.0)
    .extrude(height)
)

# Second ring body ("New Body") - identical concentric dimensions as specified,
# so it coincides exactly with the first ring.
ring2 = (
    cq.Workplane("XY")
    .circle(outer_d / 2.0)
    .circle(inner_d / 2.0)
    .extrude(height)
)

# Both rings occupy the same space; the resulting geometry is a single
# 80/60 mm ring, 20 mm tall.
result = ring1
