import cadquery as cq
import math

turns = 5
r0, r1 = 40.0, 32.5
rise_per_turn = 8.0
amp = 2.5
periods = 6 * turns          # 30 wave periods along the whole path
quarter = 1.0 / periods / 4.0  # quarter period in normalized parameter

def smooth(x):
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)

def env(t):
    # decay in first and last quarter period
    return min(smooth(t / quarter), smooth((1 - t) / quarter))

N = 20 * periods
ts = [i / N for i in range(N + 1)]

# rise: uniform 8 mm/turn with the rise rate ramped to zero at the ends
dt = 1.0 / N
cum = [0.0]
for i in range(1, N + 1):
    tm = (ts[i] + ts[i - 1]) / 2
    cum.append(cum[-1] + env(tm) * dt)
norm = cum[-1]
total_rise = rise_per_turn * turns

pts = []
for i, t in enumerate(ts):
    th = 2 * math.pi * turns * t
    r = r0 + (r1 - r0) * t
    z = total_rise * cum[i] / norm + amp * env(t) * math.sin(2 * math.pi * periods * t)
    pts.append(cq.Vector(r * math.cos(th), r * math.sin(th), z))

path_edge = cq.Edge.makeSpline(pts)
path = cq.Workplane("XY").add(path_edge)

# profile on the plane at the start of the path (XZ plane, start point at (40,0,0)):
# 8 mm wide side horizontal (parallel to XY), 1.2 mm thick
profile = cq.Workplane("XZ").center(r0, 0).rect(8.0, 1.2)

result = profile.sweep(cq.Workplane("XY").add(cq.Wire.assembleEdges([path_edge])), isFrenet=False)
