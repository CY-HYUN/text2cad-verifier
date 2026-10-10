import cadquery as cq
import math

r = 3.0
half_t = 2.0
H = 25.0
plate_t = 5.0
R_plate = 40.0

t0 = 0.7
t1 = 6 * math.pi
N = 700

def inv(t):
    return (r * (math.cos(t) + t * math.sin(t)), r * (math.sin(t) - t * math.cos(t)))

outer = []
inner = []
for i in range(N + 1):
    t = t0 + (t1 - t0) * i / N
    x, y = inv(t)
    nx, ny = math.sin(t), -math.cos(t)
    outer.append((x + half_t * nx, y + half_t * ny))
    inner.append((x - half_t * nx, y - half_t * ny))

pts = outer + inner[::-1]

wall = (cq.Workplane("XY").workplane(offset=plate_t)
        .polyline(pts).close().extrude(H))

# rounded start cap (radius 2, tangent to both wall sides)
sx, sy = inv(t0)
cap = (cq.Workplane("XY").workplane(offset=plate_t)
       .center(sx, sy).circle(half_t).extrude(H))
wall = wall.union(cap)

# clip the wall to the plate outline
clip = cq.Workplane("XY").circle(R_plate).extrude(plate_t + H)
wall = wall.intersect(clip)

plate = cq.Workplane("XY").circle(R_plate).extrude(plate_t)

result = plate.union(wall)
