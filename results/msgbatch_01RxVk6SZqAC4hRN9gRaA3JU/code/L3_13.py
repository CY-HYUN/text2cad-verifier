import cadquery as cq
import math

# Parameters
m = 3.0
z = 20
alpha = math.radians(20.0)
d = m * z                    # pitch diameter 60
db = d * math.cos(alpha)     # base diameter
rb = db / 2.0
ra = 66.0 / 2.0              # tip radius
rf = 52.5 / 2.0              # root radius
width = 30.0

inv = lambda a: math.tan(a) - a
half_base = math.pi / (2 * z) + inv(alpha)   # half tooth angle at base circle
t_max = math.sqrt((ra / rb) ** 2 - 1)

def involute_pt(t):
    x = 0.5 * db * (math.cos(t) + t * math.sin(t))
    y = 0.5 * db * (math.sin(t) - t * math.cos(t))
    return x, y

def rot(p, a):
    c, s = math.cos(a), math.sin(a)
    return (p[0] * c - p[1] * s, p[0] * s + p[1] * c)

N = 12
# Lower flank (involute rotated so it starts at -half_base), mirrored for upper flank
lower = [rot(involute_pt(t_max * i / N), -half_base) for i in range(N + 1)]
upper = [(p[0], -p[1]) for p in reversed(lower)]

a_tip_lo = math.atan2(lower[-1][1], lower[-1][0])
a_tip_hi = -a_tip_lo

pts = []
pitch = 2 * math.pi / z
for k in range(z):
    base = k * pitch
    tooth = []
    # root -> base circle radial line
    tooth.append((rf * math.cos(-half_base), rf * math.sin(-half_base)))
    tooth += lower
    # tip arc
    for i in range(1, 4):
        a = a_tip_lo + (a_tip_hi - a_tip_lo) * i / 4
        tooth.append((ra * math.cos(a), ra * math.sin(a)))
    tooth += upper
    tooth.append((rf * math.cos(half_base), rf * math.sin(half_base)))
    # root arc to next tooth
    a0 = half_base
    a1 = pitch - half_base
    for i in range(1, 4):
        a = a0 + (a1 - a0) * i / 4
        tooth.append((rf * math.cos(a), rf * math.sin(a)))
    pts += [rot(p, base) for p in tooth]

gear = cq.Workplane("XY").polyline(pts).close().extrude(width)

# Grooves (recess) on both end faces, dia 45, depth 3
groove = cq.Workplane("XY").circle(45.0 / 2).extrude(3.0)
gear = gear.cut(groove).cut(groove.translate((0, 0, width - 3.0)))

# Bore with keyway 6 x 3
bore = cq.Workplane("XY").circle(10.0).extrude(width)
key = cq.Workplane("XY").center(0, (10.0 + 3.0) / 2.0).rect(6.0, 13.0 - 0.0).extrude(width)
key = cq.Workplane("XY").box(6.0, 13.0, width, centered=(True, False, False))
gear = gear.cut(bore.union(key))

result = gear
