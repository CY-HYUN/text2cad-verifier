import math

R = 20.0
H = 60.0

prism = cq.Workplane("XY").polygon(8, 2 * R).extrude(H)

# 45-degree cone for the pointed top
profile = [(0, 0), (R, 0), (R, 40), (0, 60)]
cone = (cq.Workplane("XZ").polyline(profile).close()
        .revolve(360, (0, 0, 0), (0, 1, 0)))
body = prism.intersect(cone)

# Rectangular groove around the middle: 5 wide, 2 deep
apothem = R * math.cos(math.pi / 8)
inner_R = (apothem - 2) / math.cos(math.pi / 8)
outer = cq.Workplane("XY").workplane(offset=27.5).polygon(8, 2 * (R + 5)).extrude(5)
inner = cq.Workplane("XY").workplane(offset=27.5).polygon(8, 2 * inner_R).extrude(5)
ring = outer.cut(inner)

result = body.cut(ring)
