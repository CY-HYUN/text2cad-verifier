import cadquery as cq
import math

turns = 5
r0, r1 = 40.0, 32.5
pitch = 8.0
amp = 2.5
periods_per_turn = 6
nper = turns * periods_per_turn
q = 1.0 / (4.0 * nper)  # quarter period in t


def smooth(u):
    u = max(0.0, min(1.0, u))
    return u * u * (3 - 2 * u)


def env(t):
    return min(smooth(t / q), smooth((1 - t) / q))


N = nper * 12
pts = []
z_base = 0.0
prev_t = 0.0
for i in range(N + 1):
    t = i / N
    if i > 0:
        # rise rate decays to zero at both ends
        z_base += 0.5 * (env(t) + env(prev_t)) * pitch * turns * (t - prev_t)
    prev_t = t
    th = 2 * math.pi * turns * t
    r = r0 + (r1 - r0) * t
    z = z_base + amp * env(t) * math.sin(2 * math.pi * nper * t)
    pts.append(cq.Vector(r * math.cos(th), r * math.sin(th), z))

path = cq.Workplane("XY").spline(pts)

profile = cq.Workplane("XZ").center(r0, 0).rect(8.0, 1.2)

result = profile.sweep(path, isFrenet=True)
