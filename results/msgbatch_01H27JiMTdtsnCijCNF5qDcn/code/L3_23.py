import cadquery as cq
import math

L, W, H = 200.0, 100.0, 80.0

# Base block: X 0..200, Y 0..100, Z 0..80
result = cq.Workplane("XY").box(L, W, H, centered=False)

# Internal longitudinal main oil passage (along Y) at center height
main_x = L / 2
main = (cq.Workplane("XZ").workplane(offset=0)
        .center(main_x, H / 2).circle(8).extrude(-W))  # XZ normal is -Y, so negative extrude goes +Y
result = result.cut(main)

# Three horizontal inlet holes from front face (y=0), dia 20, at center height
inlet_xs = [40, 100, 160]
inlet_depth = 55
for x in inlet_xs:
    h = (cq.Workplane("XZ").center(x, H / 2).circle(10).extrude(-inlet_depth))
    result = result.cut(h)

# Cross passage along X at y=50 connecting inlets' ends and main passage
cross = (cq.Workplane("YZ").center(50, H / 2).circle(8).extrude(L))
result = result.cut(cross)

# Two rows of five 10 mm holes from top, down to cross passage (z=40)
row_ys = [30, 70]
xs = [20 + i * 40 for i in range(5)]
pts = [(x, y) for y in row_ys for x in xs]
# Rows at y=30 and 70 : drill down to depth reaching main passage network
top_holes = (cq.Workplane("XY").workplane(offset=H).pushPoints(pts)
             .circle(5).extrude(-(H / 2 + 2)))
result = result.cut(top_holes)
# Connect row holes to the network via longitudinal channels along X at each row
for y in row_ys:
    ch = cq.Workplane("YZ").center(y, H / 2).circle(5).extrude(L)
    result = result.cut(ch)

# Countersunk bolt holes at four corners
corner_pts = [(12, 12), (L - 12, 12), (12, W - 12), (L - 12, W - 12)]
result = (result.faces(">Z").workplane(origin=(0, 0, H))
          .pushPoints([(x - L / 2, y - W / 2) for x, y in corner_pts])
          .cskHole(9, 16, 90))

# Oval lightening grooves: two on the bottom, two on the sides (avoiding flow channels)
# Bottom ovals (cut upward from z=0)
for x in [60, 140]:
    slot = (cq.Workplane("XY").center(x, 50).slot2D(40, 12, 90).extrude(15))
    result = result.cut(slot)
# Side ovals on the right/left faces (x=0 and x=L), at low height away from channels
for x0, d in [(0, 1), (L, -1)]:
    slot = (cq.Workplane("YZ").workplane(offset=x0 - (0 if d == 1 else 12))
            .center(50, 12).slot2D(40, 10, 0).extrude(12))
    result = result.cut(slot)
