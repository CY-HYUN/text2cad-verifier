import cadquery as cq
import math

# Base disc: diameter 80, thickness 5
base = cq.Workplane("XY").circle(40.0).extrude(5.0)

# Involute of base circle rb = 3, wall thickness d = 4 (offset along the normal)
rb = 3.0
d = 4.0
t_end = 12.0
n = 80

def inv(t):
    return (rb * (math.cos(t) + t * math.sin(t)),
            rb * (math.sin(t) - t * math.cos(t)))

def off(t):
    x, y = inv(t)
    return (x + d * math.sin(t), y - d * math.cos(t))

ts = [t_end * i / n for i in range(n + 1)]
p1 = [inv(t) for t in ts]   # one wall face
p2 = [off(t) for t in ts]   # offset wall face

# End caps (arcs): bulge backward at the center, forward at the outer end
def mid_cap(a, b, t, sign):
    mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
    return (mx + sign * (d / 2) * math.cos(t), my + sign * (d / 2) * math.sin(t))

mid_start = mid_cap(p1[0], p2[0], 0.0, -1)
mid_end = mid_cap(p1[-1], p2[-1], t_end, 1)

p2r = p2[::-1]

wall = (
    cq.Workplane("XY").workplane(offset=5.0)
    .moveTo(*p1[0])
    .spline(p1[1:], includeCurrent=True)
    .threePointArc(mid_end, p2[-1])
    .spline(p2r[1:], includeCurrent=True)
    .threePointArc(mid_start, p1[0])
    .close()
    .extrude(25.0)
)

result = base.union(wall)
