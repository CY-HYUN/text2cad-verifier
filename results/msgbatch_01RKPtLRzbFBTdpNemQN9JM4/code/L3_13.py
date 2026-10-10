import cadquery as cq
import math

m = 3.0
z = 20
alpha = math.radians(20)
width = 30.0
rp = m * z / 2.0
rb = rp * math.cos(alpha)
ra = 33.0
rr = 26.25

def inv(r):
    t = math.sqrt((r / rb) ** 2 - 1)
    return t - math.atan(t)

inv_p = inv(rp)
half = math.pi / (2 * z)
pitch = 2 * math.pi / z

def pol(r, a):
    return (r * math.cos(a), r * math.sin(a))

N = 8
pts = []
for k in range(z):
    rot = k * pitch
    # right flank (angle negative side), root to tip
    right = [(rr, -half - inv_p)]
    for i in range(N + 1):
        r = rb + (ra - rb) * i / N
        right.append((r, -half - inv_p + inv(r)))
    for r, a in right:
        pts.append(pol(r, a + rot))
    # tip mid
    pts.append(pol(ra, rot))
    # left flank mirrored, tip to root
    for r, a in reversed(right):
        pts.append(pol(r, -a + rot))
    # root gap mid point
    a_end = half + inv_p
    a_next = pitch - half - inv_p
    pts.append(pol(rr, rot + (a_end + a_next) / 2))

body = cq.Workplane("XY").polyline(pts).close().extrude(width)

# protruding hub
hub = cq.Workplane("XY").workplane(offset=-2).circle(16).extrude(width + 4)
# weight-reducing grooves on both faces
groove = (cq.Workplane("XY").circle(22.5).circle(16).extrude(5))
groove2 = (cq.Workplane("XY").workplane(offset=width - 5).circle(22.5).circle(16).extrude(5))
body = body.cut(groove).cut(groove2).union(hub)

# bore and keyway
bore = cq.Workplane("XY").workplane(offset=-5).circle(10).extrude(width + 10)
key = cq.Workplane("XY").workplane(offset=-5).center(6.5, 0).rect(13, 6).extrude(width + 10)
result = body.cut(bore).cut(key)
