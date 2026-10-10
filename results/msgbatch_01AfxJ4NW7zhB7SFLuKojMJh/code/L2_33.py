import cadquery as cq
import math

# base plate
plate = cq.Workplane("XY").box(100, 100, 5, centered=(True, True, False))

# slots
ys = [-30, -15, 0, 15, 30]
for y in ys:
    cutter = cq.Workplane("XY").box(80, 10, 5, centered=(True, True, False)).translate((0, y, 0))
    plate = plate.cut(cutter)

# deflector blades
angle = 30
for y in ys:
    blade = (cq.Workplane("XY")
             .box(80, 12, 2, centered=(True, False, False))
             .rotate((0, 0, 0), (1, 0, 0), angle)
             .translate((0, y + 5, 5)))
    plate = plate.union(blade)

result = plate
