import cadquery as cq
import math

turns = 5
r0, r1 = 40.0, 32.5
pitch = 8.0
amp = 2.5
periods_per_turn = 6
nper = turns * periods_per_turn
q = 1.0 / (4.0 * nper)  # quarter period in normalized parameter t


def smooth(u):
    u = max(0.0, min(1.0, u))
    return u * u * (3 - 2 * u)


def env(t):
    # smooth decay over first / last quarter period
    return min(smooth(t / q), smooth((1 - t) / q))


N = nper * 16

# normalise the rise-rate envelope so total rise is exactly pitch * turns
ts = [i / N for i in range(N + 1)]
cum = [0.0]
for i in range(1, N + 1):
    cum.append(cum[-1] + 0.5 * (env(ts[i]) + env(ts[i - 1])) * (ts[i] - ts[i - 1]))
total = cum[-1]

pts = []
for i in range(N + 1):
    t = ts[i]
    th = 2 * math.pi * turns * t
    r = r0 + (r1 - r0) * t
    z_base = pitch * turns * cum[i] / total
    z = z_base + amp * env(t) * math.sin(2 * math.pi * nper * t)
    pts.append(cq.Vector(r * math.cos(th), r * math.sin(th), z))

path = cq.Workplane("XY").spline(pts)

# Rectangle at path start: 8.0 radial (horizontal), 1.2 thick (vertical)
profile = cq.Workplane("XZ").center(r0, 0).rect(8.0, 1.2)

# fixed binormal = Z keeps the long side horizontal along the whole sweep
result = profile.sweep(path, normal=(0, 0, 1))
