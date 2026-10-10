import cadquery as cq
import math

# Base plate
plate = cq.Workplane("XY").box(100, 100, 5, centered=(True, True, False))

# Five through-slots: 80 long (X), 10 wide (Y), 5 mm gaps
pitch = 15
ys = [(i - 2) * pitch for i in range(5)]
for yc in ys:
    cutter = (cq.Workplane("XY").box(80, 10, 5, centered=(True, True, False))
              .translate((0, yc, 0)))
    plate = plate.cut(cutter)

# Inclined deflector blades: 80 x 12 x 2, hinged at the slot edge on the top face
angle = 30
result = plate
for yc in ys:
    blade = (cq.Workplane("XY").box(80, 12, 2, centered=(True, False, False))
             .rotate((0, 0, 0), (1, 0, 0), angle)
             .translate((0, yc - 5, 5)))
    result = result.union(blade)
