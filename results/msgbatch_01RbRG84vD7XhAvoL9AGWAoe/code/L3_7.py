import cadquery as cq
import math

# Parameters
rb = 3.0          # base circle radius
t_end = 6 * math.pi   # 1080 degrees
half = 2.0        # half wall thickness (4 mm wall)
H = 25.0          # wall height
plate_d = 80.0
plate_t = 5.0

def side(t, s):
    # involute offset: base point + (r*t + s) * normal
    c = (rb * math.cos(t), rb * math.sin(t))
    n = (math.sin(t), -math.cos(t))
    k = rb * t + s
    return (c[0] + k * n[0], c[1] + k * n[1])

# start angle where inner offset is non-degenerate (avoid cusp loop)
t0 = half / rb
N = 300
ts = [t0 + (t_end - t0) * i / (N - 1) for i in range(N)]
outer = [side(t, +half) for t in ts]
inner = [side(t, -half) for t in ts]

# semicircular cap at start, centred on the involute centerline point
cx, cy = side(t0, 0.0)
mid = (cx - half * math.cos(t0), cy - half * math.sin(t0))

wall = (
    cq.Workplane("XY").workplane(offset=plate_t)
    .moveTo(*inner[0])
    .threePointArc(mid, outer[0])
    .spline(outer[1:], includeCurrent=True)
    .lineTo(*inner[-1])
    .spline(list(reversed(inner[:-1])), includeCurrent=True)
    .close()
    .extrude(H)
)

# keep wall within plate
clip = cq.Workplane("XY").circle(plate_d / 2).extrude(plate_t + H)
wall = wall.intersect(clip)

plate = cq.Workplane("XY").circle(plate_d / 2).extrude(plate_t)

result = plate.union(wall)
