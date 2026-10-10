import cadquery as cq

# Overall dimensions
top_size = 100.0
top_t = 5.0
leg_d = 10.0
leg_h = 50.0
base_outer = 100.0
base_inner = 80.0
base_t = 5.0

# Legs sit centred on the base frame ring (ring width is 10 mm)
leg_off = (base_outer / 2 + base_inner / 2) / 2  # 45 mm from centre

# Base frame: z from 0 to base_t
base = (
    cq.Workplane("XY")
    .rect(base_outer, base_outer)
    .rect(base_inner, base_inner)
    .extrude(base_t)
)

# Four legs: z from base_t to base_t + leg_h
pts = [(sx * leg_off, sy * leg_off) for sx in (-1, 1) for sy in (-1, 1)]
legs = (
    cq.Workplane("XY")
    .workplane(offset=base_t)
    .pushPoints(pts)
    .circle(leg_d / 2)
    .extrude(leg_h)
)

# Top plate
top_z = base_t + leg_h
top = (
    cq.Workplane("XY")
    .workplane(offset=top_z)
    .rect(top_size, top_size)
    .extrude(top_t)
)

# Corner brackets under the top plate, on the inner side of each leg
blk = 14.0
blk_h = 6.0
blk_c = leg_off - 4.0
brackets = (
    cq.Workplane("XY")
    .workplane(offset=top_z - blk_h)
    .pushPoints([(sx * blk_c, sy * blk_c) for sx in (-1, 1) for sy in (-1, 1)])
    .rect(blk, blk)
    .extrude(blk_h)
)

result = base.union(legs).union(brackets).union(top)
