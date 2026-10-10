import cadquery as cq
import math

# Base disk: diameter 80, height 15
disk = cq.Workplane("XY").circle(40.0).extrude(15.0)

# Cross slots on top surface (z=15), width 10, length 90 (> diameter), depth 5
slot_len = 90.0
slot_w = 10.0
depth = 5.0

slot1 = (cq.Workplane("XY").workplane(offset=15.0 - depth)
         .rect(slot_len, slot_w).extrude(depth))
slot2 = (cq.Workplane("XY").workplane(offset=15.0 - depth)
         .rect(slot_w, slot_len).extrude(depth))

result = disk.cut(slot1).cut(slot2)
