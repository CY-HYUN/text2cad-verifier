import cadquery as cq

# Overall dimensions
W = 100.0
top_t = 5.0
leg_d = 10.0
leg_h = 50.0
base_t = 5.0
inner = 80.0

# Base frame (bottom), z from 0 to base_t
base = (
    cq.Workplane("XY")
    .rect(W, W).extrude(base_t)
    .cut(cq.Workplane("XY").rect(inner, inner).extrude(base_t))
)

# Legs centered within frame band (band width 10 -> center at 45)
off = (W + inner) / 4.0  # 45
pts = [(off, off), (-off, off), (off, -off), (-off, -off)]
legs = (
    cq.Workplane("XY").workplane(offset=base_t)
    .pushPoints(pts).circle(leg_d / 2).extrude(leg_h)
)

# Corner blocks under top plate (extending features on inner corners)
blk = 14.0
blk_h = 5.0
bpts = [(sx * (W / 2 - blk / 2), sy * (W / 2 - blk / 2)) for sx in (1, -1) for sy in (1, -1)]
blocks = (
    cq.Workplane("XY").workplane(offset=base_t + leg_h - blk_h)
    .pushPoints(bpts).rect(blk, blk).extrude(blk_h)
)

# Top plate
top = (
    cq.Workplane("XY").workplane(offset=base_t + leg_h)
    .rect(W, W).extrude(top_t)
)

result = base.union(legs).union(blocks).union(top)
