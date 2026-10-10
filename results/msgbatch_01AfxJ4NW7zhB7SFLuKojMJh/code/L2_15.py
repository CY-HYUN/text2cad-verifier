import cadquery as cq
import math

T = 10
disc = cq.Workplane("XY").circle(40).extrude(T)

cutters = None
for i in range(4):
    a = i * 90
    slot = (cq.Workplane("XY").center(32, 0).rect(26, 8).extrude(T)
            .union(cq.Workplane("XY").center(19, 0).circle(4).extrude(T)))
    slot = slot.rotate((0, 0, 0), (0, 0, 1), a)
    cutters = slot if cutters is None else cutters.union(slot)

    b = a + 45
    cx = 40 * math.cos(math.radians(b))
    cy = 40 * math.sin(math.radians(b))
    arc = cq.Workplane("XY").center(cx, cy).circle(20).extrude(T)
    cutters = cutters.union(arc)

result = disc.cut(cutters)
result = result.cut(cq.Workplane("XY").circle(5).extrude(T))
