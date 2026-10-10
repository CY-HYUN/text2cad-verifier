import cadquery as cq
import math

# Base plate
L, W, T = 100.0, 100.0, 5.0
plate = cq.Workplane("XY").box(L, W, T, centered=(True, True, False))

# Slots
slot_len, slot_w, gap = 80.0, 10.0, 5.0
n = 5
pitch = slot_w + gap
centers = [(i - (n - 1) / 2.0) * pitch for i in range(n)]

for yc in centers:
    cutter = (cq.Workplane("XY")
              .box(slot_len, slot_w, T * 3, centered=True)
              .translate((0, yc, T / 2)))
    plate = plate.cut(cutter)

# Deflector blades (80 x 12 x 2), hinged at upper edge of each slot, sloping over it
blade_len, blade_w, blade_t = 80.0, 12.0, 2.0
angle = 30.0  # tilt from horizontal

result = plate
for yc in centers:
    blade = (cq.Workplane("XY")
             .box(blade_len, blade_w, blade_t, centered=False)
             .translate((-blade_len / 2, -blade_w, 0))   # y from -12..0, z 0..2
             .rotate((0, 0, 0), (1, 0, 0), -angle)         # free edge lifts upward
             .translate((0, yc + slot_w / 2 + 1.0, T - 0.3)))  # slight embed for solid union
    result = result.union(blade)
