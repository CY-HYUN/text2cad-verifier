import cadquery as cq
import math

plate = cq.Workplane("XY").box(100, 100, 5, centered=(True, True, False))

pitch = 15
n = 5
ys = [(i - (n - 1) / 2) * pitch for i in range(n)]

# cut slots 80 x 10
for y0 in ys:
    slot = (cq.Workplane("XY").center(0, y0)
            .rect(80, 10).extrude(5))
    plate = plate.cut(slot)

# baffle profile (12 x 2) tilted 45 degrees, hinged at slot upper edge
c = math.cos(math.radians(45))
s = math.sin(math.radians(45))
w, t = 12.0, 2.0
dx, dz = -c, s   # width direction (toward -Y, up)
nx, nz = s, c    # thickness direction

for y0 in ys:
    ye = y0 + 5
    p0 = (ye, 2.5)
    p1 = (p0[0] + w * dx, p0[1] + w * dz)
    p2 = (p1[0] + t * nx, p1[1] + t * nz)
    p3 = (p0[0] + t * nx, p0[1] + t * nz)
    baffle = (cq.Workplane("YZ")
              .polyline([p0, p1, p2, p3]).close()
              .extrude(40, both=True))
    plate = plate.union(baffle)

result = plate
