import cadquery as cq
import math

# Base plate
L, W, T = 100.0, 100.0, 5.0
plate = cq.Workplane("XY").box(L, W, T, centered=(True, True, False))

# Slots
slot_len, slot_w, gap = 80.0, 10.0, 5.0
pitch = slot_w + gap
n = 5
ycs = [(i - (n - 1) / 2) * pitch for i in range(n)]

slots = None
for yc in ycs:
    s = cq.Workplane("XY").box(slot_len, slot_w, T * 3).translate((0, yc, T / 2))
    slots = s if slots is None else slots.union(s)
plate = plate.cut(slots)

# Inclined deflector blades (rain louvers)
bl_len, bl_w, bl_t = 80.0, 12.0, 2.0
angle = 30.0  # inclination from horizontal

result = plate
for yc in ycs:
    blade = (
        cq.Workplane("XY")
        .box(bl_len, bl_w, bl_t, centered=(True, False, False))
        .translate((0, -bl_w, 0))           # spans y -12..0, z 0..2
        .rotate((0, 0, 0), (1, 0, 0), -angle)  # tilt up over the slot
        .translate((0, yc + slot_w / 2 + 0.5, T - 0.5))  # hinge at upper slot edge
    )
    result = result.union(blade)
