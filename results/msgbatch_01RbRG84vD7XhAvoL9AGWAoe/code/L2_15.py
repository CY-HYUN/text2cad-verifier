import cadquery as cq
import math

R = 40.0
T = 10.0
slot_w = 8.0
slot_len = 25.0
cut_r = 20.0
hole_d = 10.0

body = cq.Workplane("XY").circle(R).extrude(T)

# U-shaped radial slots
bottom_r = R - slot_len  # 15
c_r = bottom_r + slot_w / 2.0  # center of semicircular bottom
for i in range(4):
    ang = i * 90.0
    rect_len = (R + 5) - c_r
    box = (cq.Workplane("XY")
           .center(c_r + rect_len / 2.0, 0)
           .rect(rect_len, slot_w)
           .extrude(T)
           .rotate((0, 0, 0), (0, 0, 1), ang))
    cyl = (cq.Workplane("XY")
           .center(c_r, 0)
           .circle(slot_w / 2.0)
           .extrude(T)
           .rotate((0, 0, 0), (0, 0, 1), ang))
    body = body.cut(box).cut(cyl)

# Semicircular cutouts between slots
for i in range(4):
    a = math.radians(45 + i * 90)
    cut = (cq.Workplane("XY")
           .center(R * math.cos(a), R * math.sin(a))
           .circle(cut_r)
           .extrude(T))
    body = body.cut(cut)

# Central shaft hole
hole = cq.Workplane("XY").circle(hole_d / 2.0).extrude(T)
body = body.cut(hole)

result = body
