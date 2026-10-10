import cadquery as cq
import math

# Start with a base workplane
wp = cq.Workplane("front")

# Create the meridional rib cross-section (a small rectangle)
rib_profile = cq.Workplane("front").sketch()
rib_profile = rib_profile.rect(3, 4).finalize()

# Create the semi-ellipse path for the rib sweep
# Semi-ellipse with semi-major axis 60 (along Y) and semi-minor axis 40 (along X)
semi_major = 60
semi_minor = 40
num_points = 100

# Generate semi-ellipse points (from -X axis, going up in Y, to +X axis)
ellipse_points = []
for i in range(num_points + 1):
    t = i * math.pi / num_points  # t goes from 0 to pi for semi-ellipse
    x = semi_minor * math.cos(t)
    y = semi_major * math.sin(t)
    ellipse_points.append((x, y, 0))

# Create a 3D wire/edge from the ellipse points
ellipse_edge = cq.Edge.makeSpline(ellipse_points)

# Create one rib by sweeping the profile along the ellipse path
rib_one = cq.Workplane("front").sweep(rib_profile, ellipse_edge)

# Create the base ellipsoid through revolution
# Create the semi-ellipse profile as a 2D sketch
base_sketch = cq.Workplane("front").sketch()
for i in range(len(ellipse_points) - 1):
    base_sketch = base_sketch.segment((ellipse_points[i][0], ellipse_points[i][1]), 
                                       (ellipse_points[i+1][0], ellipse_points[i+1][1]))
base_sketch = base_sketch.finalize()

ellipsoid = cq.Workplane("front").revolve(360, (0, 1, 0), (0, 0, 0), base_sketch)

# Circular pattern the rib 12 times around the Y-axis
ribs = rib_one
for i in range(1, 12):
    angle = i * 360 / 12
    rib_copy = rib_one.rotate((0, 0, 0), (0, 1, 0), angle)
    ribs = ribs.union(rib_copy)

# Create horizontal datum planes and latitudinal rings
rings_solid = None

for y_pos in [30, 0, -30]:
    # Calculate the outer diameter at this Y position on the ellipsoid
    if abs(y_pos) <= semi_major:
        x_radius = semi_minor * math.sqrt(1 - (y_pos / semi_major) ** 2)
    else:
        x_radius = 0
    
    outer_dia = 2 * x_radius
    inner_dia = max(0, outer_dia - 3)
    
    # Create annular sketch on the plane at Y = y_pos
    ring_wp = cq.Workplane("XZ").workplane(offset=y_pos)
    ring_sketch = ring_wp.sketch()
    ring_sketch = ring_sketch.circle(outer_dia / 2)
    if inner_dia > 0.1:
        ring_sketch = ring_sketch.circle(inner_dia / 2)
    ring_sketch = ring_sketch.finalize()
    
    # Extrude the ring by 4mm (2mm on each side of the plane)
    ring = ring_wp.extrude(4, both=True)
    
    if rings_solid is None:
        rings_solid = ring
    else:
        rings_solid = rings_solid.union(ring)

# Combine all solids
result = ellipsoid.union(ribs)
if rings_solid is not None:
    result = result.union(rings_solid)

# Cut out the top through-hole (cylinder along Y-axis with radius 15mm)
hole = cq.Workplane("front").circle(15).extrude(200, both=True)
result = result.cut(hole)
