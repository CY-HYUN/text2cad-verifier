import cadquery as cq
import math

# Parameters
m = 3.0
z = 20
alpha = math.radians(20.0)
thk = 15.0
rp = m * z / 2.0             # 30
rb = rp * math.cos(alpha)    # 28.19
ra = rp + m                  # 33
rf = rp - 1.25 * m           # 26.25
fillet_r = 0.9

def inv(a):
    return math.tan(a) - a

# Half tooth angle at base circle (tooth thickness pi*m/2 at pitch circle)
half_b = math.pi / (2 * z) + inv(alpha)

# Flank (polar) samples from root to tip
flank = [(rf, half_b)]
n_inv = 12
for k in range(n_inv + 1):
    r = rb + (ra - rb) * k / n_inv
    ar = math.acos(min(1.0, rb / r))
    flank.append((r, half_b - inv(ar)))
a_tip = flank[-1][1]

def pol(r, a):
    return (r * math.cos(a), r * math.sin(a))

pts = []
pitch = 2 * math.pi / z
for i in range(z):
    phi = pitch * i
    # right flank root -> tip
    for r, a in flank:
        pts.append(pol(r, phi - a))
    # tip arc
    for k in range(1, 4):
        a = -a_tip + 2 * a_tip * k / 4
        pts.append(pol(ra, phi + a))
    # left flank tip -> root
    for r, a in reversed(flank):
        pts.append(pol(r, phi + a))
    # root arc to next tooth
    a0 = phi + half_b
    a1 = phi + pitch - half_b
    for k in range(1, 5):
        pts.append(pol(rf, a0 + (a1 - a0) * k / 5))

vecs = [cq.Vector(x, y, 0) for x, y in pts]
wire = cq.Wire.makePolygon(vecs + [vecs[0]])

# Root fillet via offset out/in (rounds concave root corners)
try:
    w2 = wire.offset2D(fillet_r, "arc")[0].offset2D(-fillet_r, "arc")[0]
    face = cq.Face.makeFromWires(w2)
    gear_solid = cq.Solid.extrudeLinear(face, cq.Vector(0, 0, thk))
    gear = cq.Workplane("XY").add(gear_solid)
    if not gear_solid.isValid():
        raise ValueError
except Exception:
    gear = cq.Workplane("XY").polyline(pts).close().extrude(thk)

# Center bore and keyway
bore_d = 20.0
key_w = 6.0
key_d = 3.0
cutter = cq.Workplane("XY").circle(bore_d / 2).extrude(thk)
key = (cq.Workplane("XY")
       .center(0, bore_d / 2 + key_d / 2 - 1.0)
       .rect(key_w, key_d + 2.0)
       .extrude(thk))
cutter = cutter.union(key)

result = gear.cut(cutter)
