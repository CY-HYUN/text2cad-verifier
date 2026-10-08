import cadquery as cq

# Base rectangular prism: 60 x 40 footprint, 40 tall (z from 0 to 40)
body = cq.Workplane("XY").box(60, 40, 40, centered=(True, True, False))

# Two vertical blind holes from the top face: Ø10, 30 deep, 30 mm apart
body = (
    body.faces(">Z").workplane()
    .pushPoints([(-15, 0), (15, 0)])
    .hole(10, 30)
)

# Horizontal side channel: Ø10, entering from the +X side face.
# Its axis is at z = 15, so the channel spans z = 10..20 and overlaps
# the bottoms of both vertical holes (which end at z = 10).
# It runs from x = 30 back to x = -20, fully crossing both holes.
channel = (
    cq.Workplane("YZ")
    .workplane(offset=-20)
    .center(0, 15)
    .circle(5)
    .extrude(50)
)

result = body.cut(channel)
