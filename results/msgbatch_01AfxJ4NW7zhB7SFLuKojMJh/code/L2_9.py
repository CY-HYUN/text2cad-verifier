import cadquery as cq
import math

R_out = 40.0
R_in = 25.0
H = 10.0
tip = 45.0
n = 12
pitch = 360.0 / n

ring = (cq.Workplane("XY").circle(R_out).circle(R_in).extrude(H))

def pt(r, a):
    return (r * math.cos(math.radians(a)), r * math.sin(math.radians(a)))

pts = [pt(38, 0), pt(tip, 0), pt(R_out, pitch), pt(38, pitch)]
tooth = cq.Workplane("XY").polyline(pts).close().extrude(H)

result = ring
for i in range(n):
    t = tooth.rotate((0, 0, 0), (0, 0, 1), i * pitch)
    result = result.union(t)
