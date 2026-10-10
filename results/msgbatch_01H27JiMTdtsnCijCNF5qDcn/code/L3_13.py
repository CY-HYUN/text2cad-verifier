import cadquery as cq
import math

m = 3
z = 20
alpha = math.radians(20)
d = m * z
db = d * math.cos(alpha)
rb = db / 2
r_tip = 33.0
r_root = 26.25
r_in = 25.0
T = 30.0

def inv_pt(t):
    return (rb * (math.cos(t) + t * math.sin(t)), rb * (math.sin(t) - t * math.cos(t)))

tp = math.sqrt((d / 2 / rb) ** 2 - 1)
offset = (tp - math.atan(tp)) + math.pi / (2 * z)
tmax = math.sqrt((r_tip / rb) ** 2 - 1)

def rot(p, a):
    c, s = math.cos(a), math.sin(a)
    return (p[0] * c - p[1] * s, p[0] * s + p[1] * c)

N = 12
lower = [rot(inv_pt(tmax * i / N), -offset) for i in range(N + 1)]
upper = [(x, -y) for x, y in lower]

a0 = math.atan2(lower[0][1], lower[0][0])
inner_low = (r_in * math.cos(a0), r_in * math.sin(a0))
inner_up = (inner_low[0], -inner_low[1])

w = cq.Workplane("XY").moveTo(*inner_low)
for p in lower:
    w = w.lineTo(*p)
w = w.threePointArc((r_tip, 0), upper[-1])
for p in reversed(upper):
    w = w.lineTo(*p)
w = w.lineTo(*inner_up).close()
tooth = w.extrude(T)

gear = cq.Workplane("XY").circle(r_root).extrude(T)
for i in range(z):
    gear = gear.union(tooth.rotate((0, 0, 0), (0, 0, 1), i * 360.0 / z))

# grooves on both faces
groove_bot = cq.Workplane("XY").circle(22.5).extrude(3.0)
groove_top = cq.Workplane("XY").workplane(offset=T - 3.0).circle(22.5).extrude(3.0)
gear = gear.cut(groove_bot).cut(groove_top)

# bore with keyway
bore = cq.Workplane("XY").circle(10.0).extrude(T)
key = cq.Workplane("XY").center(0, 11.5).rect(6, 3 + 10 - 8 + 0.0 + 1.0 * 0 + 0).extrude(T)
key = cq.Workplane("XY").moveTo(-3, 0).lineTo(3, 0).lineTo(3, 13).lineTo(-3, 13).close().extrude(T)
gear = gear.cut(bore).cut(key)

result = gear
