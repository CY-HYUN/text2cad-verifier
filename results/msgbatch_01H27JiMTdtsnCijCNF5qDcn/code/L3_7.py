import cadquery as cq
import math

# Base disc
base = cq.Workplane("XY").circle(40.0).extrude(5.0)

rb = 3.0
off = 4.0
tmax = 11.0
n = 150

def A(t):
    return (rb * (math.cos(t) + t * math.sin(t)),
            rb * (math.sin(t) - t * math.cos(t)))

def B(t):
    x, y = A(t)
    return (x + off * math.sin(t), y - off * math.cos(t))

ts = [tmax * i / n for i in range(n + 1)]
ptsA = [A(t) for t in ts]
ptsB = [B(t) for t in ts]

# end arc midpoint (outer end, bulging along the tangent)
a_end, b_end = ptsA[-1], ptsB[-1]
mid_end = ((a_end[0] + b_end[0]) / 2 + 2 * math.cos(tmax),
           (a_end[1] + b_end[1]) / 2 + 2 * math.sin(tmax))
# center end arc midpoint (bulging backwards)
a0, b0 = ptsA[0], ptsB[0]
mid_start = ((a0[0] + b0[0]) / 2 - 2.0, (a0[1] + b0[1]) / 2)

wp = (cq.Workplane("XY").workplane(offset=5.0)
      .moveTo(*ptsA[0])
      .spline(ptsA[1:], includeCurrent=True)
      .threePointArc(mid_end, ptsB[-1])
      .spline(ptsB[::-1][1:], includeCurrent=True)
      .threePointArc(mid_start, ptsA[0])
      .close())

wall = wp.extrude(25.0)

result = base.union(wall)
