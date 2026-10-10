import cadquery as cq
import math

rb = 3.0
half = 2.0
t0 = 1.0
t1 = 6 * math.pi
n = 300

def P(t):
    return (rb * (math.cos(t) + t * math.sin(t)), rb * (math.sin(t) - t * math.cos(t)))

def side(t, s):
    x, y = P(t)
    return (x + s * half * math.sin(t), y - s * half * math.cos(t))

ts = [t0 + (t1 - t0) * i / n for i in range(n + 1)]
ptsA = [side(t, 1) for t in ts]
ptsB = [side(t, -1) for t in ts]

px, py = P(t0)
mid = (px - half * math.cos(t0), py - half * math.sin(t0))

wall_sketch = (
    cq.Workplane("XY").workplane(offset=5)
    .moveTo(*ptsA[0])
    .spline(ptsA[1:], includeCurrent=True)
    .lineTo(*ptsB[-1])
    .spline(list(reversed(ptsB))[1:], includeCurrent=True)
    .threePointArc(mid, ptsA[0])
    .close()
)
wall = wall_sketch.extrude(25)

disk = cq.Workplane("XY").circle(40).extrude(5)
clip = cq.Workplane("XY").circle(40).extrude(30)

result = disk.union(wall.intersect(clip))
