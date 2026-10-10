import cadquery as cq
import math

# Parameters
m = 3  # module
z = 20  # number of teeth
alpha = 20  # pressure angle in degrees
alpha_rad = math.radians(alpha)

# Calculated parameters
D = m * z  # pitch circle diameter = 60
Db = D * math.cos(alpha_rad)  # base circle diameter ≈ 56.38
rb = Db / 2  # base circle radius

# Tooth parameters
tooth_thickness_pitch = math.pi * m / 2
pitch_radius = D / 2

# Create the involute curve for one tooth flank
def involute_x(t, rb):
    return rb * (math.cos(t) + t * math.sin(t))

def involute_y(t, rb):
    return rb * (math.sin(t) - t * math.cos(t))

# Calculate the involute parameter t at the pitch circle
def find_involute_t_at_radius(target_r, rb, initial_t=0.5):
    t = initial_t
    for _ in range(20):
        x = involute_x(t, rb)
        y = involute_y(t, rb)
        r = math.sqrt(x**2 + y**2)
        if abs(r - target_r) < 0.01:
            break
        t = t + (target_r - r) / (rb + 1)
    return t

t_pitch = find_involute_t_at_radius(pitch_radius, rb)

# Create cylindrical blank
blank = cq.Workplane("XY").circle(pitch_radius).extrude(15.0)

# Create one tooth space as a sketch
tooth_angle_rad = 2 * math.pi / z
half_tooth_angle_rad = tooth_angle_rad / 2

# Build involute curve for tooth flank
points_one_side = []
num_points = 40
for i in range(num_points + 1):
    t = t_pitch * i / num_points
    x = involute_x(t, rb)
    y = involute_y(t, rb)
    points_one_side.append((x, y))

# Create a single tooth space by mirroring the involute
tooth_space_pts = []

# Involute on right side
for pt in points_one_side:
    x_rot = pt[0] * math.cos(half_tooth_angle_rad) - pt[1] * math.sin(half_tooth_angle_rad)
    y_rot = pt[0] * math.sin(half_tooth_angle_rad) + pt[1] * math.cos(half_tooth_angle_rad)
    tooth_space_pts.append((x_rot, y_rot))

# Involute on left side (mirrored)
for pt in reversed(points_one_side):
    x_rot = pt[0] * math.cos(-half_tooth_angle_rad) - pt[1] * math.sin(-half_tooth_angle_rad)
    y_rot = pt[0] * math.sin(-half_tooth_angle_rad) + pt[1] * math.cos(-half_tooth_angle_rad)
    tooth_space_pts.append((x_rot, y_rot))

# Create tooth space sketch
tooth_sketch = cq.Workplane("XY").moveTo(tooth_space_pts[0][0], tooth_space_pts[0][1])
for pt in tooth_space_pts[1:]:
    tooth_sketch = tooth_sketch.lineTo(pt[0], pt[1])
tooth_sketch = tooth_sketch.close()

# Create a 2D tooth space profile and extrude as a cut
tooth_space_face = tooth_sketch.extrude(15.0)

# Cut the tooth space and array 20 times around the blank
gear = blank
for i in range(z):
    angle = 360 * i / z
    tooth_space_rotated = tooth_space_face.rotate((0, 0, 0), (0, 0, 1), angle)
    gear = gear.cut(tooth_space_rotated)

# Add center hole (10mm diameter)
gear = gear.faces(">Z").workplane().circle(10.0).cutThruAll()

# Add keyway on the end face (6mm x 3mm)
keyway_w = 6.0
keyway_h = 3.0
gear = gear.faces(">Z").workplane().rect(keyway_w, keyway_h).cutThruAll()

# Apply fillet at root of teeth
gear = gear.edges("|Z").fillet(0.9)

result = gear
