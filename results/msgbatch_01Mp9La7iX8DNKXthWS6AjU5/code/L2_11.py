import cadquery as cq

# Block 60x40x40, centered in XY, base at z=0
block = cq.Workplane("XY").rect(60, 40).extrude(40)

# Two vertical blind holes from top, 30 deep
holes = (
    cq.Workplane("XY").workplane(offset=40)
    .pushPoints([(-15, 0), (15, 0)])
    .circle(5)
    .extrude(-30)
)

# Horizontal channel from side face x=-30, axis at z=15, running along +X
channel = (
    cq.Workplane("YZ").workplane(offset=-30)
    .center(0, 15)
    .circle(5)
    .extrude(50)  # from x=-30 to x=20, penetrating both holes
)

result = block.cut(holes).cut(channel)
