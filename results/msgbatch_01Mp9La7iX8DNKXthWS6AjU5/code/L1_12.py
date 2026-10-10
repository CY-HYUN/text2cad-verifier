import cadquery as cq
import math

disk = cq.Workplane("XY").circle(45.0).extrude(15.0)
result = (
    disk.faces(">Z").workplane()
    .rect(30.0, 30.0)
    .cutThruAll()
)
