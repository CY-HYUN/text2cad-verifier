import cadquery as cq
import math

R = 40.0
T = 10.0
slot_w = 8.0
slot_len = 25.0
cut_r = 20.0
hole_d = 10.0

# Main disc with central shaft hole
disc = cq.Workplane("XY").circle(R).circle(hole_d / 2).extrude(T)

# Four radial U-slots (open at rim, semicircular bottom pointing to center)
r_bottom = R - slot_len           # 15 mm from center
r_arc_c = r_bottom + slot_w / 2   # center of semicircle
outer = R + 5.0
for i in range(4):
    a = i * 90.0
    rect_len = outer - r_arc_c
    rect = (cq.Workplane("XY")
            .center(r_arc_c + rect_len / 2, 0)
            .rect(rect_len, slot_w)
            .extrude(T))
    arc = (cq.Workplane("XY")
           .center(r_arc_c, 0)
           .circle(slot_w / 2)
           .extrude(T))
    cutter = rect.union(arc).rotate((0, 0, 0), (0, 0, 1), a)
    disc = disc.cut(cutter)

# Four semicircular cutouts R20 centered on the circumference between slots
for i in range(4):
    a = math.radians(45 + i * 90)
    cx, cy = R * math.cos(a), R * math.sin(a)
    c = cq.Workplane("XY").center(cx, cy).circle(cut_r).extrude(T)
    disc = disc.cut(c)

result = disc
