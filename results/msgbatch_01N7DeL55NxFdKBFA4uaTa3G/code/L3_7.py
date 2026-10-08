import cadquery as cq
import math

# Base disc
base_d = 80.0
base_h = 5.0
base = cq.Workplane("XY").circle(base_d / 2).extrude(base_h)

# Involute wall parameters
R = 3.0          # base circle radius
d = 4.0          # wall thickness
t_end = 6 * math.pi
t_start = d / R + 0.6   # start beyond where offset curve self-intersects
wall_h = 25.0
N = 400

outer = []
inner = []
for i in range(N + 1):
    t = t_start + (t_end - t_start) * i / N
    c, s = math.cos(t), math.sin(t)
    # outer involute
    outer.append((R * (c + t * s), R * (s - t * c)))
    # inward offset by d along the normal (-sin t, cos t)
    k = R * t - d
    inner.append((R * c + k * s, R * s - k * c))

pts = outer + inner[::-1]

wall = (
    cq.Workplane("XY")
    .workplane(offset=base_h)
    .polyline(pts)
    .close()
    .extrude(wall_h)
)

result = base.union(wall)
