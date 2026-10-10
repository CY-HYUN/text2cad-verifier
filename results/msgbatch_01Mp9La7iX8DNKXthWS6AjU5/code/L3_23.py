import cadquery as cq
import math

L, W, H = 200.0, 100.0, 80.0

# Base block (centered in XY, z from 0 to H)
result = cq.Workplane("XY").box(L, W, H, centered=(True, True, False))

# Internal longitudinal main oil passage (along Y, at center height, x=0 would be between holes)
# Use a main passage along X at mid-width, at center height, connecting inlets
main_d = 16.0
main = (cq.Workplane("YZ").workplane(offset=-L/2 + 10)
        .center(0, H/2).circle(main_d/2).extrude(L - 20))
result = result.cut(main)

# Three front inlet holes (from front face y=-W/2 going +Y), dia 20, at center height
inlet_x = [-60.0, 0.0, 60.0]
for x in inlet_x:
    h = (cq.Workplane("XZ", origin=(0, -W/2, 0))
         .center(x, H/2).circle(10.0).extrude(-(W/2 + 10)))
    result = result.cut(h)

# Two rows of five 10 mm holes on top, cut downward to main passage level
xs = [-80, -40, 0, 40, 80]
rows = [-20.0, 20.0]
# Cross passages in Y direction at each x column linking rows with main passage
for x in xs:
    for y in rows:
        hole = (cq.Workplane("XY", origin=(0, 0, H))
                .center(x, y).circle(5.0).extrude(-(H/2 + 5)))
        result = result.cut(hole)
# Internal connecting passages along Y at center height for each row column
for x in xs:
    cross = (cq.Workplane("XZ", origin=(0, -30, 0))
             .center(x, H/2).circle(4.0).extrude(-60))
    result = result.cut(cross)

# Four countersunk corner mounting holes
for sx in (-1, 1):
    for sy in (-1, 1):
        cx, cy = sx * (L/2 - 12), sy * (W/2 - 12)
        result = result.cut(
            cq.Workplane("XY", origin=(0, 0, 0)).center(cx, cy)
            .circle(4.5).extrude(H))
        cone = cq.Solid.makeCone(4.5, 9.0, 4.5,
                                 pnt=cq.Vector(cx, cy, H - 4.5),
                                 dir=cq.Vector(0, 0, 1))
        result = result.cut(cq.Workplane("XY").add(cone))

# Four oval weight-reduction grooves: two on bottom, two on sides
# Bottom ovals
for x in (-50.0, 50.0):
    slot = (cq.Workplane("XY").center(x, 0).slot2D(40, 12, 90).extrude(15))
    result = result.cut(slot)
# Side ovals (on the back face y=+W/2), blind from the back, below the flow level
for x in (-50.0, 50.0):
    slot = (cq.Workplane("XZ", origin=(0, W/2, 0)).center(x, 12)
            .slot2D(40, 10, 0).extrude(15))
    result = result.cut(slot)
