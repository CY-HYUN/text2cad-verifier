import cadquery as cq
import math

R = 20.0          # circumradius of octagon
H = 60.0          # main body height
tip = 20.0        # 45-degree cone height (equal to radius)

# Octagonal prism extended to tip height
octo = cq.Workplane("XY").polygon(8, 2 * R).extrude(H + tip)

# Limiting shape: cylinder for body + 45 deg cone on top
cyl = cq.Workplane("XY").circle(R + 1).extrude(H)
cone = cq.Workplane("XY").add(
    cq.Solid.makeCone(R, 0, tip, cq.Vector(0, 0, H), cq.Vector(0, 0, 1))
)
limit = cyl.union(cone)

body = octo.intersect(limit)

# Horizontal groove around the middle: 5 wide, 2 deep (measured from flat faces)
apothem = R * math.cos(math.radians(22.5))
inner_R = (apothem - 2.0) / math.cos(math.radians(22.5))
gw = 5.0
zc = H / 2.0
ring = (
    cq.Workplane("XY").workplane(offset=zc - gw / 2)
    .polygon(8, 2 * (R + 2)).extrude(gw)
    .cut(
        cq.Workplane("XY").workplane(offset=zc - gw / 2)
        .polygon(8, 2 * inner_R).extrude(gw)
    )
)

result = body.cut(ring)
