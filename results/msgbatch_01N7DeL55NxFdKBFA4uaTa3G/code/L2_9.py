import cadquery as cq
import math

# Ring parameters
R_out = 40.0   # 80 mm diameter
R_in = 25.0    # 50 mm diameter
T = 10.0       # thickness

# Base ring
ring = (
    cq.Workplane("XY")
    .circle(R_out)
    .circle(R_in)
    .extrude(T)
)

# Single ratchet tooth: radial 5 mm line, then a slanted line back to the outer circle
tooth_h = 5.0
span = math.radians(25.0)  # angular span of the slanted face
r_overlap = 38.0           # small overlap into the ring for a clean merge

pts = [
    (r_overlap, 0.0),
    (R_out + tooth_h, 0.0),                               # tip of radial line
    (R_out * math.cos(span), R_out * math.sin(span)),     # slanted line back to circumference
    (r_overlap * math.cos(span), r_overlap * math.sin(span)),
]

tooth = cq.Workplane("XY").polyline(pts).close().extrude(T)

# Circular array of 12 teeth
result = ring
n = 12
for i in range(n):
    result = result.union(tooth.rotate((0, 0, 0), (0, 0, 1), i * 360.0 / n))
