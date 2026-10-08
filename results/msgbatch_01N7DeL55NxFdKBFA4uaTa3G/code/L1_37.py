import cadquery as cq

# Disk
disk = cq.Workplane("XY").circle(40.0).extrude(15.0)

# Cross slots on top surface, 10 mm wide, 5 mm deep
slot_len = 100.0
slot1 = cq.Workplane("XY").workplane(offset=10.0).rect(slot_len, 10.0).extrude(5.0)
slot2 = cq.Workplane("XY").workplane(offset=10.0).rect(10.0, slot_len).extrude(5.0)

result = disk.cut(slot1).cut(slot2)
