import cadquery as cq
import math

# Create the base cylinder
# Start with Top plane and draw a circle with diameter 80mm, extrude by 5mm
base = cq.Workplane("XY").circle(40).extrude(5)

# Generate involute curve parametrically
# Involute with base circle radius R=3, parameter t from 0 to 6π
# X(t) = (R + width) * (cos(t) + t * sin(t))
# Y(t) = (R + width) * (sin(t) - t * cos(t))
# where width = 4 for the outer wall

R = 3
width = 4
num_points = 200
t_values = [i * 6 * math.pi / num_points for i in range(num_points + 1)]

# Generate outer involute curve
outer_points = []
for t in t_values:
    x = (R + width) * (math.cos(t) + t * math.sin(t))
    y = (R + width) * (math.sin(t) - t * math.cos(t))
    outer_points.append((x, y))

# Generate inner involute curve (offset inward by 4mm, so radius becomes just R)
inner_points = []
for t in t_values:
    x = R * (math.cos(t) + t * math.sin(t))
    y = R * (math.sin(t) - t * math.cos(t))
    inner_points.append((x, y))

# Create the spiral ring sketch on the top face at z=5
spiral_ring_sketch = (
    cq.Workplane("XY")
    .workplane(offset=5)
    .spline(outer_points, includeCurrent=False)
    .spline(list(reversed(inner_points)), includeCurrent=False)
    .close()
)

# Extrude the spiral ring by 25mm
spiral_ring = spiral_ring_sketch.extrude(25)

# Combine base and spiral ring into one solid
result = base.union(spiral_ring)
