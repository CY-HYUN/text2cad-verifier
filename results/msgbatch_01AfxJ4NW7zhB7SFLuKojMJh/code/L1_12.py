import cadquery as cq
import math

result = (
    cq.Workplane("XY")
    .circle(45)
    .extrude(15)
    .faces(">Z")
    .workplane()
    .rect(30, 30)
    .cutThruAll()
)
