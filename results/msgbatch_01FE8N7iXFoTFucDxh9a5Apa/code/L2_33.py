import cadquery as cq
import math

# Base plate
L, W, T = 100.0, 100.0, 5.0
plate = cq.Workplane("XY").box(L, W, T, centered=(True, True, False))

# Slots
slot_len, slot_w, gap = 80.0, 10.0, 5.0
n = 5
pitch = slot_w + gap
ys = [(i - (n - 1) / 2) * pitch for i in range(n)]

for yc in ys:
    cutter = (cq.Workplane("XY")
              .box(slot_len, slot_w, T * 3)
              .translate((0, yc, T / 2)))
    plate = plate.cut(cutter)

# Sloped rain deflector blades
blade_len, blade_w, blade_t = 80.0, 12.0, 2.0
angle = 30.0  # inclination from horizontal

for yc in ys:
    blade = (cq.Workplane("XY")
             .box(blade_len, blade_w, blade_t, centered=(True, False, False))
             .translate((0, -blade_w, 0))          # y in [-12, 0], z in [0, 2]
             .rotate((0, 0, 0), (1, 0, 0), -angle)  # free edge tilts upward over slot
             .translate((0, yc + slot_w / 2 + 1.0, T - 0.5)))
    plate = plate.union(blade)

result = plate
