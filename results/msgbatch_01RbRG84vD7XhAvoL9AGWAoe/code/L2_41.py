import cadquery as cq
import math

R = 20.0
H = 60.0

# Main octagonal prism
body = cq.Workplane("XY").polygon(8, 2 * R).extrude(H)

# Top extension: octagonal prism intersected with a 45-degree cone -> pointed top
ext_h = R  # 45 degrees: height equals radius
ext = cq.Workplane("XY").workplane(offset=H).polygon(8, 2 * R).extrude(ext_h)
cone = cq.Workplane("XY").add(
    cq.Solid.makeCone(R, 0, ext_h, cq.Vector(0, 0, H), cq.Vector(0, 0, 1))
)
top = ext.intersect(cone)
body = body.union(top)

# Horizontal rectangular groove around the middle: 5 wide, 2 deep
apothem = R * math.cos(math.pi / 8)
inner_R = (apothem - 2.0) / math.cos(math.pi / 8)
gw = 5.0
outer_ring = (
    cq.Workplane("XY").workplane(offset=H / 2 - gw / 2)
    .polygon(8, 2 * (R + 5)).extrude(gw)
)
inner_core = (
    cq.Workplane("XY").workplane(offset=H / 2 - gw / 2)
    .polygon(8, 2 * inner_R).extrude(gw)
)
groove = outer_ring.cut(inner_core)
body = body.cut(groove)

result = body
