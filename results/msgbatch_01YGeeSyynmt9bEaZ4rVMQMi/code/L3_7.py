import cadquery as cq
import math

# ---- Parameters ----
base_d = 80.0
base_t = 5.0
R = 3.0            # involute base circle radius
wall = 4.0         # wall thickness (offset)
wall_h = 25.0
t_max = 6 * math.pi
N = 600

# ---- Base disc ----
base = cq.Workplane("XY").circle(base_d / 2).extrude(base_t)

# ---- Involute wall profile ----
def inv(t):
    return (R * (math.cos(t) + t * math.sin(t)),
            R * (math.sin(t) - t * math.cos(t)))

outer = []
inner = []
for i in range(N + 1):
    t = t_max * i / N
    x, y = inv(t)
    outer.append((x, y))
    # offset along normal (-sin t, cos t) by wall thickness
    inner.append((x - wall * math.sin(t), y + wall * math.cos(t)))

pts = outer + inner[::-1]

wall_solid = (
    cq.Workplane("XY")
    .workplane(offset=base_t)
    .polyline(pts)
    .close()
    .extrude(wall_h)
)

# Cut off the outer end with an arc (the disc boundary)
clip = (
    cq.Workplane("XY")
    .workplane(offset=base_t)
    .circle(base_d / 2)
    .extrude(wall_h)
)
wall_solid = wall_solid.intersect(clip)

# ---- Merge ----
result = base.union(wall_solid)
