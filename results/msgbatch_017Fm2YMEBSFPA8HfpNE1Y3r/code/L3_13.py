import cadquery as cq
import math

# Global variables
m = 3  # module
z = 20  # number of teeth
pressure_angle = math.radians(20)  # pressure angle in radians

# Calculate diameters
d = m * z  # pitch circle diameter = 60
db = d * math.cos(pressure_angle)  # base circle diameter

# Generate involute profile points for one side of tooth
def involute_profile(db, t_max=0.4, num_points=50):
    points = []
    for i in range(num_points):
        t = i * t_max / num_points
        x = 0.5 * db * (math.cos(t) + t * math.sin(t))
        y = 0.5 * db * (math.sin(t) - t * math.cos(t))
        points.append((x, y))
    return points

# Get involute profile
involute = involute_profile(db)

# Create mirrored involute
mirrored_involute = [(-x, y) for x, y in reversed(involute)]

# Combine profiles
tooth_profile = involute + mirrored_involute

# Create gear tooth sketch
tooth_sketch = cq.Sketch()

# Draw the involute profile
tooth_sketch = tooth_sketch.polyline(involute)

# Mirror to create other side
tooth_sketch = tooth_sketch.polyline(mirrored_involute)

# Connect top with arc (tip diameter 66mm, radius 33mm)
tip_radius = 33
tooth_sketch = tooth_sketch.arc(
    (involute[-1][0], involute[-1][1]),
    (mirrored_involute[-1][0], mirrored_involute[-1][1]),
    radius=tip_radius
)

# Connect root with arc (root diameter 52.5mm, radius 26.25mm)
root_radius = 26.25
tooth_sketch = tooth_sketch.arc(
    (mirrored_involute[0][0], mirrored_involute[0][1]),
    (involute[0][0], involute[0][1]),
    radius=root_radius
)

# Close the sketch
tooth_sketch = tooth_sketch.close()

# Create workplane and attach sketch
result = cq.Workplane("XY").placeSketch(tooth_sketch)

# Extrude to form gear blank
result = result.extrude(30.0)

# Create a base disc for the gear body
result = cq.Workplane("XY").circle(33).extrude(30.0)

# Create the teeth using circular pattern
tooth_wp = cq.Workplane("XY").placeSketch(tooth_sketch).extrude(30.0)

# Create polar pattern of teeth
result = cq.Workplane("XY").circle(33).extrude(30.0)
for i in range(z):
    angle = (360.0 / z) * i
    tooth_copy = tooth_wp.rotate((0, 0, 0), (0, 0, 1), angle)
    result = result.union(tooth_copy)

# Add grooves on end faces
result = result.faces(">Z").workplane().circle(22.5).cutThruAll()
result = result.faces("<Z").workplane().circle(22.5).cutThruAll()

# Create center hole
result = result.faces(">Z").workplane().circle(10.0).cutThruAll()

# Add keyway (6x3mm rectangular slot through center)
keyway_sketch = cq.Sketch().rectangle(6, 3)
result = result.placeSketch(keyway_sketch).cutThruAll()

