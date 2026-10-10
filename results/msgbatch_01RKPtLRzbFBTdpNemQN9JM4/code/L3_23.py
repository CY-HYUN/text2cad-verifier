import cadquery as cq
import math

L, W, H = 200.0, 100.0, 80.0
block = cq.Workplane("XY").box(L, W, H, centered=(True, True, False))

# Internal main horizontal channel along X
main = (cq.Workplane("YZ").workplane(offset=-90).center(0, 40)
        .circle(8).extrude(180))
block = block.cut(main)

# 3 inlets on front face (y=-50), dia 20, running into the main channel
for x in (-60, 0, 60):
    inlet = (cq.Workplane("XZ").workplane(offset=50)  # plane at y=-50, normal -Y
             .center(x, 40).circle(10).extrude(-50))
    block = block.cut(inlet)

# Two rows of 5 vertical outlets (10 total), dia 10, from top down to the channel
for y in (-8, 8):
    for x in (-80, -40, 0, 40, 80):
        out = (cq.Workplane("XY").workplane(offset=36)
               .center(x, y).circle(5).extrude(44))
        block = block.cut(out)

# Countersunk (counterbored) corner mounting holes
for sx in (-1, 1):
    for sy in (-1, 1):
        x, y = sx * 90, sy * 40
        thru = cq.Workplane("XY").center(x, y).circle(4.5).extrude(H)
        cb = (cq.Workplane("XY").workplane(offset=H - 6)
              .center(x, y).circle(7.5).extrude(6))
        block = block.cut(thru).cut(cb)

# 4 oval weight-reduction grooves from the bottom
for sx in (-1, 1):
    for sy in (-1, 1):
        slot = (cq.Workplane("XY").center(sx * 45, sy * 33)
                .slot2D(50, 14, 0).extrude(20))
        block = block.cut(slot)

result = block
