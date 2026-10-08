import cadquery as cq
import math

# Base plate
plate_L, plate_W, plate_T = 100.0, 100.0, 5.0
slot_L, slot_W = 80.0, 10.0
baffle_W, baffle_T = 12.0, 2.0
angle = 45.0
n, pitch = 5, 15.0

result = cq.Workplane("XY").box(plate_L, plate_W, plate_T, centered=(True, True, False))

ys = [(i - (n - 1) / 2.0) * pitch for i in range(n)]

# Cut slots
for yc in ys:
    slot = (cq.Workplane("XY")
            .box(slot_L, slot_W, plate_T * 3, centered=(True, True, True))
            .translate((0, yc, plate_T / 2.0)))
    result = result.cut(slot)

# Baffles hinged at the upper edge of each slot, tilted 45 degrees
for yc in ys:
    baffle = (cq.Workplane("XY")
              .box(slot_L, baffle_W, baffle_T, centered=False)
              .translate((-slot_L / 2.0, -baffle_W, -baffle_T)))
    baffle = (baffle.rotate((0, 0, 0), (1, 0, 0), -angle)
              .translate((0, yc + slot_W / 2.0, plate_T)))
    result = result.union(baffle)
