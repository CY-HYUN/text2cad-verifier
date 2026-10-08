import cadquery as cq
import math

m = 3.0
N = 20
alpha = math.radians(20)
width = 15.0
rp = m * N / 2.0
rb = rp * math.cos(alpha)
ra = rp + m
rf = rp - 1.25 * m
rfil = 0.9
bore_r = 10.0
key_w = 6.0
key_h = 3.0

def inv(a):
    return math.tan(a) - a

half_space = math.pi / N
psi_b = math.pi / (2 * N) + inv(alpha)

def psi(r):
    ar = math.acos(rb / r)
    return math.pi / (2 * N) + inv(alpha) - inv(ar)

def polar(r, t):
    return (r * math.cos(t), r * math.sin(t))

# upper half of one tooth: from tooth center line (angle 0) to space center (angle pi/N)
upper = []
# tip land
nt = 4
for i in range(nt + 1):
    upper.append(polar(ra, psi(ra) * i / nt))
# involute flank
ni = 20
for i in range(1, ni + 1):
    r = ra - (ra - rb) * i / ni
    upper.append(polar(r, psi(r)))
# radial flank + root fillet
rc = rf + rfil
r_t1 = math.sqrt(rc ** 2 - rfil ** 2)
phi_c = psi_b + math.asin(rfil / rc)
if r_t1 < rb - 1e-6:
    upper.append(polar(r_t1, psi_b))
C = polar(rc, phi_c)
T1 = polar(r_t1, psi_b)
T2 = polar(rf, phi_c)
a1 = math.atan2(T1[1] - C[1], T1[0] - C[0])
a2 = math.atan2(T2[1] - C[1], T2[0] - C[0])
da = a2 - a1
while da > math.pi:
    da -= 2 * math.pi
while da < -math.pi:
    da += 2 * math.pi
nf = 8
for i in range(1, nf + 1):
    a = a1 + da * i / nf
    p = (C[0] + rfil * math.cos(a), C[1] + rfil * math.sin(a))
    if math.atan2(p[1], p[0]) < half_space - 1e-6:
        upper.append(p)
# root arc to space center
if phi_c < half_space - 1e-6:
    nr = 3
    for i in range(1, nr + 1):
        t = phi_c + (half_space - phi_c) * i / nr
        upper.append(polar(rf, t))
else:
    upper.append(polar(math.hypot(*upper[-1]), half_space))

# full tooth: lower half (mirrored, reversed) + upper half
lower = [(x, -y) for (x, y) in reversed(upper)]
tooth = lower[:-1] + upper[:-1]  # drop duplicate center & last (space center shared)

pts = []
for k in range(N):
    th = 2 * math.pi * k / N
    c, s = math.cos(th), math.sin(th)
    for (x, y) in tooth:
        pts.append((x * c - y * s, x * s + y * c))

# remove near-duplicates
clean = []
for p in pts:
    if not clean or math.hypot(p[0] - clean[-1][0], p[1] - clean[-1][1]) > 1e-4:
        clean.append(p)
if math.hypot(clean[0][0] - clean[-1][0], clean[0][1] - clean[-1][1]) < 1e-4:
    clean.pop()

gear = cq.Workplane("XY").polyline(clean).close().extrude(width)

# bore + keyway (keyway aligned with a tooth space at angle pi/N)
bore = cq.Workplane("XY").circle(bore_r).extrude(width)
key_len = bore_r + key_h
key = (cq.Workplane("XY")
       .center(key_len / 2.0, 0)
       .rect(key_len, key_w)
       .extrude(width)
       .rotate((0, 0, 0), (0, 0, 1), math.degrees(half_space)))

result = gear.cut(bore).cut(key)
