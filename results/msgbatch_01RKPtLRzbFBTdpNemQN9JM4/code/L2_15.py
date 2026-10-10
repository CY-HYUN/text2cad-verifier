import cadquery as cq
import math

T = 10
result = cq.Workplane("XY").circle(40).extrude(T)

# slots
for i in range(4):
    a = i * 90
    slot = (cq.Workplane("XY")
            .center(0, 0)
            .moveTo(19, -4).lineTo(46, -4).lineTo(46, 4).lineTo(19, 4)
            .threePointArc((15, 0), (19, -4))
            .close()
            .extrude(T))
    slot = slot.rotate((0, 0, 0), (0, 0, 1), a)
    result = result.cut(slot)

# circular cutouts between slots
for i in range(4):
    a = math.radians(45 + i * 90)
    x, y = 40 * math.cos(a), 40 * math.sin(a)
    c = cq.Workplane("XY").center(x, y).circle(20).extrude(T)
    result = result.cut(c)

# center hole
result = result.cut(cq.Workplane("XY").circle(5).extrude(T))
