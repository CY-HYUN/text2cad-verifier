import cadquery as cq
import math

m = 3.0
z = 20
pa = math.radians(20)
W = 15.0
rp = m * z / 2
rb = rp * math.cos(pa)
ra = rp + m
rr = rp - 1.25 * m  # 26.25
rf = 0.9


def inv(a):
    return math.tan(a) - a


def pol(r, a):
    return (r * math.cos(a), r * math.sin(a))


half_p = math.pi / (2 * z) + inv(pa)  # half tooth angle at base
half_b = half_p


def half_r(r):
    al = math.acos(min(1.0, rb / r))
    return math.pi / (2 * z) + inv(pa) - inv(al)


def fillet_pts(th0, s, n=6):
    # arc from root circle tangent point to radial-line tangent point
    rc = rr + rf
    d = math.asin(rf / rc)
    c = th0 + s * d
    C = pol(rc, c)
    Pr = pol(rr, c)
    Pl = pol(rc * math.cos(d), th0)
    a1 = math.atan2(Pr[1] - C[1], Pr[0] - C[0])
    a2 = math.atan2(Pl[1] - C[1], Pl[0] - C[0])
    da = (a2 - a1 + math.pi) % (2 * math.pi) - math.pi
    return [(C[0] + rf * math.cos(a1 + da * k / n), C[1] + rf * math.sin(a1 + da * k / n)) for k in range(n + 1)]


def rot(p, phi):
    c, s = math.cos(phi), math.sin(phi)
    return (p[0] * c - p[1] * s, p[0] * s + p[1] * c)


# one tooth centered on angle 0
right_f = fillet_pts(-half_b, -1)
left_f = [(x, -y) for (x, y) in right_f][::-1]  # mirrored, order line->root
# right flank
pts = list(right_f)
pts.append(pol(rb, -half_b))
N = 14
for k in range(1, N + 1):
    r = rb + (ra - rb) * k / N
    pts.append(pol(r, -half_r(r)))
# tip arc
ht = half_r(ra)
for k in range(1, 4):
    pts.append(pol(ra, -ht + 2 * ht * k / 4))
# left flank
for k in range(N, 0, -1):
    r = rb + (ra - rb) * k / N
    pts.append(pol(r, half_r(r)))
pts.append(pol(rb, half_b))
pts.extend(left_f)

# root arc points between teeth
step = 2 * math.pi / z
a_start = math.atan2(left_f[-1][1], left_f[-1][0])
a_end = math.atan2(right_f[0][1], right_f[0][0]) + step
root_mid = [pol(rr, a_start + (a_end - a_start) * k / 4) for k in range(1, 4)]

allpts = []
for i in range(z):
    phi = i * step
    tooth = pts + root_mid
    allpts.extend([rot(p, phi) for p in tooth])

gear = cq.Workplane("XY").polyline(allpts).close().extrude(W)

hole = cq.Workplane("XY").circle(10).extrude(W)
key = (cq.Workplane("XY").center(6.5, 0).rect(13, 6).extrude(W)
       .rotate((0, 0, 0), (0, 0, 1), math.degrees(math.pi / z)))

result = gear.cut(hole).cut(key)
