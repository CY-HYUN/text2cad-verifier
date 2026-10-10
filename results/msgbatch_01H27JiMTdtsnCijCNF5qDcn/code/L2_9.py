import cadquery as cq
import math

# Ring: OD 80, ID 50, height 10
ring = cq.Workplane("XY").circle(40).circle(25).extrude(10)

# Single ratchet tooth: radial 5 mm line from the outer circumference,
# then a slanted line back to the outer circumference (30 deg pitch)
R = 40.0
a = math.radians(30)
p0 = (R, 0)
p1 = (R + 5, 0)
p2 = (R * math.cos(a), R * math.sin(a))

# Sketch on the ring's end face (z=10) and extrude 10 mm into the ring
tooth = (
    cq.Workplane("XY").workplane(offset=10)
    .polyline([p0, p1, p2]).close()
    .extrude(-10)
)

result = ring.union(tooth)

# Circular array: 12 teeth in total
for i in range(1, 12):
    result = result.union(tooth.rotate((0, 0, 0), (0, 0, 1), i * 30))
