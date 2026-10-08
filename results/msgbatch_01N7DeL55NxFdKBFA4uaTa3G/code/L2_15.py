import cadquery as cq
import math

R = 40.0
T = 10.0

result = cq.Workplane("XY").circle(R).extrude(T)

# U-shaped groove (slot) along +X, plus semicircular edge cutout in adjacent quadrant (45 deg)
slot_len = 15.0
slot_w = 8.0
slot_center_r = 22.5
cut_r = 20.0

for i in range(4):
    ang = i * 90.0
    a = math.radians(ang)
    # U-shaped slot
    sx, sy = slot_center_r * math.cos(a), slot_center_r * math.sin(a)
    slot = (cq.Workplane("XY")
            .center(sx, sy)
            .slot2D(slot_len + slot_w, slot_w, angle=ang)
            .extrude(T))
    result = result.cut(slot)
    # semicircular cutout centered on the circular edge
    b = math.radians(ang + 45.0)
    cx, cy = R * math.cos(b), R * math.sin(b)
    semi = cq.Workplane("XY").center(cx, cy).circle(cut_r).extrude(T)
    result = result.cut(semi)

# central hole
hole = cq.Workplane("XY").circle(5.0).extrude(T)
result = result.cut(hole)
