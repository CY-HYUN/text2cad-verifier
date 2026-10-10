import cadquery as cq
import math

m = 3.0
z = 20
alpha = math.radians(20.0)
d = m * z
db = d * math.cos(alpha)
rb = db / 2.0
r_tip = 33.0
r_root = 26.25
width = 30.0

# involute parameters
t_tip = math.sqrt((r_tip / rb) ** 2 - 1.0)
inv_pitch = math.tan(alpha) - alpha
delta = -math.pi / (2 * z) - inv_pitch  # rotate so the tooth is centred on the X axis

def inv_pt(t):
    x = rb * (math.cos(t) + t * math.sin(t))
    y = rb * (math.sin(t) - t * math.cos(t))
    c, s = math.cos(delta), math.sin(delta)
    return (x * c - y * s, x * s + y * c)

n = 14
lower = [inv_pt(t_tip * i / n) for i in range(n + 1)]
upper = [(x, -y) for (x, y) in reversed(lower)]

# radial lead-in from the base circle down into the root disc
p0 = lower[0]
ang0 = math.atan2(p0[1], p0[0])
r_in = 25.0
pin_low = (r_in * math.cos(ang0), r_in * math.sin(ang0))
pin_up = (pin_low[0], -pin_low[1])

tooth = (
    cq.Workplane("XY")
    .moveTo(*pin_low)
    .lineTo(*lower[0])
    .spline(lower[1:], includeCurrent=True)
    .threePointArc((r_tip, 0), upper[0])
    .spline(upper[1:], includeCurrent=True)
    .lineTo(*pin_up)
    .close()
    .extrude(width)
)

blank = cq.Workplane("XY").circle(r_root).extrude(width)

gear = blank
for i in range(z):
    gear = gear.union(tooth.rotate((0, 0, 0), (0, 0, 1), i * 360.0 / z))

# grooves (45 mm dia, 3 mm deep) on both faces
groove_bot = cq.Workplane("XY").circle(22.5).extrude(3.0)
groove_top = cq.Workplane("XY").workplane(offset=width - 3.0).circle(22.5).extrude(3.0)
gear = gear.cut(groove_bot).cut(groove_top)

# bore 20 mm with 6x3 keyway, through all
bore = cq.Workplane("XY").circle(10.0).extrude(width)
key = cq.Workplane("XY").center(0, 11.5).rect(6.0, 3.0 + 3.0 + 3.0 - 3.0 + 0.0).extrude(width)
# keyway spans y from 10-? to 13: rectangle centred at 11.5 with height 3 covers 10..13
key = cq.Workplane("XY").center(0, 11.5).rect(6.0, 3.0).extrude(width)
gear = gear.cut(bore).cut(key)

result = gear
