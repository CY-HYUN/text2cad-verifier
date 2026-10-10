import cadquery as cq
import math

# Base plate 100x100x5, centered in XY, z from 0 to 5
plate = cq.Workplane("XY").box(100, 100, 5, centered=(True, True, False))

pitch = 15
n = 5
c = math.cos(math.radians(45))
s = math.sin(math.radians(45))

# Baffle profile (in YZ plane: local x = Y, local y = Z), 12 wide x 2 thick, 45 deg
# Hinge point sits slightly inside the plate material beyond the slot's upper edge
P = (6.0, 4.0)
d = (-c, s)   # direction along the baffle width (12 mm)
t = (c, s)    # direction along the thickness (2 mm)
p1 = P
p2 = (P[0] + 12 * d[0], P[1] + 12 * d[1])
p3 = (p2[0] + 2 * t[0], p2[1] + 2 * t[1])
p4 = (P[0] + 2 * t[0], P[1] + 2 * t[1])

result = plate
for i in range(n):
    yc = (i - (n - 1) / 2) * pitch
    # 80 x 10 through slot
    slot = (cq.Workplane("XY").box(80, 10, 5, centered=(True, True, False))
            .translate((0, yc, 0)))
    result = result.cut(slot)

for i in range(n):
    yc = (i - (n - 1) / 2) * pitch
    baffle = (cq.Workplane("YZ", origin=(-40, 0, 0))
              .polyline([p1, p2, p3, p4]).close()
              .extrude(80)
              .translate((0, yc, 0)))
    result = result.union(baffle)
