import cadquery as cq
import math

R_out = 40.0
R_in = 25.0
T = 10.0
tooth_h = 5.0
n = 12
span = math.radians(25)

ring = cq.Workplane("XY").circle(R_out).circle(R_in).extrude(T)

pts = [
    (R_out, 0),
    (R_out + tooth_h, 0),
    (R_out * math.cos(span), R_out * math.sin(span)),
]
tooth = cq.Workplane("XY").polyline(pts).close().extrude(T)

result = ring
for i in range(n):
    result = result.union(tooth.rotate((0, 0, 0), (0, 0, 1), i * 360.0 / n))
