import cadquery as cq
import math

# Disk: diameter 100 mm, thickness 5 mm, base on the XY plane
disk = cq.Workplane("XY").circle(50.0).extrude(5.0)

# Concentric through hole: diameter 50 mm, cut through the full thickness
result = (
    disk.faces(">Z").workplane()
    .circle(25.0)
    .cutThruAll()
)
