import cadquery as cq

block = cq.Workplane("XY").box(60, 40, 40, centered=(True, True, False))

# vertical holes from top, down to z=10
for x in (-15, 15):
    hole = (cq.Workplane("XY").workplane(offset=10).center(x, 0)
            .circle(5).extrude(30))
    block = block.cut(hole)

# horizontal connecting channel along X at z=15
channel = (cq.Workplane("YZ").workplane(offset=-15).center(0, 15)
           .circle(5).extrude(30))
block = block.cut(channel)

result = block
