import cadquery as cq
import math

# Create the base cylinder
# Start with Top plane and draw a circle with diameter 80mm, extrude by 5mm
base = cq.Workplane("XY").circle(40).extrude(5)

# Now create the spiral/involute on the top surface
# Select the top surface for the spiral sketch
top_face = base.faces(">Z").first()

# Create a sketch on the top surface
spiral_sketch = cq.Workplane("XY").pushPoints([(0, 0)]).workplane(offset=5)

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

# Create sketch with both curves
spiral_workplane = cq.Workplane("XY").pushPoints([(0, 0)]).workplane(offset=5)

# Reverse inner points to create a closed loop
inner_points_reversed = list(reversed(inner_points))

# Combine outer and inner points to create a closed profile
closed_profile = outer_points + inner_points_reversed

# Create a face from the closed profile
# Use spline to connect the points smoothly
spiral_face = cq.Workplane("XY").spline(outer_points, includeCurrent=False)
spiral_face = spiral_face.close()

# Create the spiral sketch on top surface at z=5
spiral_sketch = cq.Workplane("XY", inPlane=cq.Plane.XY().offset(5))

# Draw outer involute as spline
spiral_sketch = spiral_sketch.spline(outer_points, includeCurrent=False)

# Draw inner involute as spline back to start
spiral_sketch = spiral_sketch.spline(inner_points_reversed, includeCurrent=False)

# Close the sketch
spiral_sketch = spiral_sketch.close()

# Get the face
spiral_profile = spiral_sketch.faces(">Z").first()

# Extrude the spiral profile by 25mm
spiral_extrusion = spiral_sketch.extrude(25)

# Create the scroll disc by using a simpler approach
# Create base circle extruded 5mm
result = cq.Workplane("XY").circle(40).extrude(5)

# Create the spiral ring sketch
# Start on the top face (z=5)
spiral_workplane = cq.Workplane("XY").pushPoints([(0, 0)]).workplane(offset=5)

# Create outer and inner spiral curves
outer_spiral = []
inner_spiral = []

for i in range(len(t_values)):
    t = t_values[i]
    outer_spiral.append((
        (R + width) * (math.cos(t) + t * math.sin(t)),
        (R + width) * (math.sin(t) - t * math.cos(t))
    ))
    inner_spiral.append((
        R * (math.cos(t) + t * math.sin(t)),
        R * (math.sin(t) - t * math.cos(t))
    ))

# Create the spiral ring profile
spiral_profile_points = outer_spiral + list(reversed(inner_spiral))

# Create sketch for spiral ring
spiral_ring_sketch = cq.Workplane("XY").workplane(offset=5).spline(
    outer_spiral, includeCurrent=False
).spline(list(reversed(inner_spiral)), includeCurrent=False).close()

# Extrude the spiral ring by 25mm
spiral_ring = spiral_ring_sketch.extrude(25)

# Combine base and spiral ring into one solid
result = result.union(spiral_ring)

