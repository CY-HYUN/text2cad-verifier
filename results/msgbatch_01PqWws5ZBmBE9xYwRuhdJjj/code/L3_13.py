import cadquery as cq
import math

# Global variables
m = 3  # module
z = 20  # number of teeth
pressure_angle = math.radians(20)  # pressure angle in radians

# Calculate diameters
d = m * z  # pitch circle diameter = 60
db = d * math.cos(pressure_angle)  # base circle diameter

# Start with a base workplane
result = cq.Workplane("XY")

# Create sketch on XY plane
sketch = result.sketch()

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

# Create one tooth profile
tooth_angle = 2 * math.pi / z

# Draw involute on one side
sketch.polyline(involute, forConstruction=False)

# Mirror to create other side
mirrored_involute = [(-x, y) for x, y in involute]
sketch.polyline(list(reversed(mirrored_involute)), forConstruction=False)

# Connect top with arc (tip diameter 66mm, radius 33mm)
tip_radius = 33
sketch.arc((involute[-1][0], involute[-1][1]), (mirrored_involute[-1][0], mirrored_involute[-1][1]), radius=tip_radius)

# Connect root with arc (root diameter 52.5mm, radius 26.25mm)
root_radius = 26.25
sketch.arc((mirrored_involute[0][0], mirrored_involute[0][1]), (involute[0][0], involute[0][1]), radius=root_radius)

# Close the sketch
sketch = sketch.close()

# Extrude sketch to form gear blank
result = result.sketch().extrude(30.0)

# Create a single tooth using polar coordinates and extrude
result = cq.Workplane("XY")
tooth_sketch = result.sketch()

# Draw basic tooth profile using simplified geometry
for i in range(50):
    t = i * 0.4 / 50
    x = 0.5 * db * (math.cos(t) + t * math.sin(t))
    y = 0.5 * db * (math.sin(t) - t * math.cos(t))
    if i == 0:
        start_point = (x, y)

tooth_points = []
for i in range(50):
    t = i * 0.4 / 50
    x = 0.5 * db * (math.cos(t) + t * math.sin(t))
    y = 0.5 * db * (math.sin(t) - t * math.cos(t))
    tooth_points.append((x, y))

# Mirror points
tooth_points_mirrored = [(-x, y) for x, y in reversed(tooth_points)]
tooth_points_all = tooth_points + tooth_points_mirrored

# Create gear body using polygon approximation
tooth_sketch.polyline(tooth_points_all, forConstruction=False)
tooth_sketch.arc((tooth_points_all[-1][0], tooth_points_all[-1][1]), 
                 (tooth_points_all[0][0], tooth_points_all[0][1]), radius=tip_radius)
tooth_sketch = tooth_sketch.close()

# Extrude tooth sketch
result = tooth_sketch.extrude(30.0)

# Circular array to create 20 teeth
result = result.polarArray(radius=1, angle=360, count=z)

# Add center bore and grooves
# Create groove on one end face
result = result.faces(">Z").workplane().circle(22.5).extrude(-3.0)

# Mirror groove on other side
result = result.faces("<Z").workplane().circle(22.5).extrude(-3.0)

# Create center hole and keyway
result = result.faces(">Z").workplane().circle(10.0).extrude(-30.0)

# Add keyway (6x3mm) - rectangular cut through center
result = result.faces(">Z").workplane().slot2D(6, 3, angle=0).extrude(-30.0)

