import cadquery as cq
import math

# Gear parameters
m = 3.0
z = 20
alpha = math.radians(20.0)
width = 30.0

r_p = m * z / 2.0              # 30
r_b = r_p * math.cos(alpha)    # base radius
r_a = r_p + m                  # 33
r_f = r_p - 1.25 * m           # 26.25

def inv(a):
    return math.tan(a) - a

# half tooth angle at base circle
beta_b = math.pi / (2 * z) + inv(alpha)

def half_angle(r):
    if r <= r_b:
        return beta_b
    a = math.acos(r_b / r)
    return beta_b - inv(a)

def pol(r, ang):
    return (r * math.cos(ang), r * math.sin(ang))

n_inv = 12
radii = [r_b + (r_a - r_b) * (i / n_inv) for i in range(n_inv + 1)]

pts = []
pitch_ang = 2 * math.pi / z
for i in range(z):
    th = i * pitch_ang
    # root point before tooth
    pts.append(pol(r_f, th - beta_b))
    # rising flank (involute)
    for r in radii:
        pts.append(pol(r, th - half_angle(r)))
    # tip arc
    h_tip = half_angle(r_a)
    for k in range(1, 4):
        pts.append(pol(r_a, th - h_tip + 2 * h_tip * k / 4))
    # descending flank
    for r in reversed(radii):
        pts.append(pol(r, th + half_angle(r)))
    pts.append(pol(r_f, th + beta_b))
    # root arc midpoint between teeth
    gap_start = th + beta_b
    gap_end = th + pitch_ang - beta_b
    for k in range(1, 3):
        pts.append(pol(r_f, gap_start + (gap_end - gap_start) * k / 3))

gear = cq.Workplane("XY").polyline(pts).close().extrude(width)

# Weight-reducing annular grooves on both faces
groove_depth = 5.0
groove = (cq.Workplane("XY").circle(45 / 2.0).circle(32 / 2.0)
          .extrude(groove_depth))
gear = gear.cut(groove)
gear = gear.cut(groove.translate((0, 0, width - groove_depth)))

# Shaft hole
hole = cq.Workplane("XY").circle(10.0).extrude(width)
gear = gear.cut(hole)

# Keyway: 6 wide, 3 deep beyond hole surface
key = (cq.Workplane("XY")
       .center((8.0 + 13.0) / 2.0, 0)
       .rect(13.0 - 8.0, 6.0)
       .extrude(width))
gear = gear.cut(key)

result = gear
