import cadquery as cq
import math

# Disk: diameter 80, height 15
disk = cq.Workplane("XY").circle(40.0).extrude(15.0)

# Cross slots on top surface (z = 15), width 10, length 100 (> diameter), depth 5
slot1 = cq.Workplane("XY").workplane(offset=10.0).rect(100.0, 10.0).extrude(5.0)
slot2 = cq.Workplane("XY").workplane(offset=10.0).rect(10.0, 100.0).extrude(5.0)

result = disk.cut(slot1).cut(slot2)
