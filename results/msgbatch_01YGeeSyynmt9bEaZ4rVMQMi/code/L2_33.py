import cadquery as cq
import math

# Base plate 100 x 100 x 5, top face at z = 5
plate = cq.Workplane("XY").box(100, 100, 5, centered=(True, True, False))

slot_len, slot_w = 80.0, 10.0
baf_w, baf_t = 12.0, 2.0
n, pitch = 5, 15.0

result = plate
for i in range(n):
    yc = (i - (n - 1) / 2) * pitch

    # Cut the slot through the plate
    slot = (cq.Workplane("XY")
            .box(slot_len, slot_w, 5, centered=(True, True, False))
            .translate((0, yc, 0)))
    result = result.cut(slot)

    # Baffle: 12 mm wide, 2 mm thick, hinged at the slot's upper edge
    baffle = (cq.Workplane("XY")
              .box(slot_len, baf_w, baf_t, centered=False)
              .translate((-slot_len / 2, -baf_w, 0))      # hinge edge on y = 0
              .rotate((0, 0, 0), (1, 0, 0), -45)          # tilt 45 deg over the slot
              .translate((0, yc + slot_w / 2, 5)))        # place at slot upper edge
    result = result.union(baffle)
