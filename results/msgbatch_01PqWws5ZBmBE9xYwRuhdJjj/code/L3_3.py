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
# The involute equations: X(t) = rb * (cos(t) + t*sin(t)), Y(t) = rb * (sin(t) - t*cos(t))
# where t ranges from 0 to the involute angle that reaches the pitch circle

def involute_x(t, rb):
    return rb * (math.cos(t) + t * math.sin(t))

def involute_y(t, rb):
    return rb * (math.sin(t) - t * math.cos(t))

# Calculate the involute parameter t at the pitch circle
# At pitch circle: x^2 + y^2 = pitch_radius^2
# Solve for t numerically by iteration
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

# Create a gear tooth profile using involute curves
def create_tooth_profile():
    # Generate involute curve points
    points = []
    num_points = 30
    for i in range(num_points + 1):
        t = t_pitch * i / num_points
        x = involute_x(t, rb)
        y = involute_y(t, rb)
        points.append((x, y))
    
    # Start building the tooth profile
    # One tooth spans 360/z degrees at pitch circle
    tooth_angle = 360 / z
    half_tooth_angle = tooth_angle / 2
    
    # Create half tooth profile by mirroring
    wp = cq.Workplane("XY")
    
    # Start from base circle, draw involute to pitch circle
    wp = wp.moveTo(points[0][0], points[0][1])
    for pt in points[1:]:
        wp = wp.lineTo(pt[0], pt[1])
    
    # Close the tooth profile
    wp = wp.close()
    
    return wp

# Create the full gear by:
# 1. Create a cylindrical blank
# 2. Create one tooth space and array it around
# 3. Apply fillets

# Create cylindrical blank
blank = cq.Workplane("XY").circle(pitch_radius).extrude(15.0)

# Create one tooth space as a sketch
tooth_angle_rad = 2 * math.pi / z
half_tooth_angle_rad = tooth_angle_rad / 2

# Create the tooth space profile
tooth_space = cq.Workplane("XY")

# Build involute curve for tooth flank
points_one_side = []
num_points = 40
for i in range(num_points + 1):
    t = t_pitch * i / num_points
    x = involute_x(t, rb)
    y = involute_y(t, rb)
    points_one_side.append((x, y))

# Create a single tooth space by mirroring the involute
# Start with the involute on one side, mirror for the other side
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

# Add center hole and keyway
gear = gear.faces(">Z").circle(10.0).extrude(-15.0, taper_angle=0)

# Add keyway on the end face
keyway_w = 6.0
keyway_h = 3.0
gear = gear.faces(">Z").workplane().rect(keyway_w, keyway_h).extrude(-15.0)

# Apply fillet at root of teeth
gear = gear.edges("|Z").fillet(0.9)

result = gear
