import cadquery as cq
import math

disc = cq.Workplane("XY").circle(40).extrude(10)

# U-shaped groove (slot open at the rim), along +X
groove = (cq.Workplane("XY")
          .center(0, 0)
          .moveTo(27, 0)
          .circle(5)
          .extrude(10))
groove_rect = cq.Workplane("XY").center(36, 0).rect(18, 10).extrude(10)
groove = groove.union(groove_rect)

# Semicircular cutout at 45 deg, centered on the edge
a = math.radians(45)
cx, cy = 40 * math.cos(a), 40 * math.sin(a)
cut_circle = cq.Workplane("XY").center(cx, cy).circle(20).extrude(10)

result = disc
for i in range(4):
    ang = 90 * i
    g = groove.rotate((0, 0, 0), (0, 0, 1), ang)
    c = cut_circle.rotate((0, 0, 0), (0, 0, 1), ang)
    result = result.cut(g).cut(c)

hole = cq.Workplane("XY").circle(5).extrude(10)
result = result.cut(hole)
