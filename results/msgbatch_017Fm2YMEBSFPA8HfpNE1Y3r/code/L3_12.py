import cadquery as cq
import math

# Create the base cylinder
base_radius = 40.0
base_height = 60.0

# Start with a cylinder on XY plane
cylinder = cq.Workplane("XY").circle(base_radius).extrude(base_height)

# Create the beveled top surface by cutting with a plane
# Cutting plane passes through (0,0,60) at 30 degrees to X-axis
# We'll use a box to cut the upper part
# The cutting plane: z = 60 + tan(30°) * y = 60 + (1/√3) * y
# At y = -40: z ≈ 37.3, at y = 40: z ≈ 82.7

cutting_box = (cq.Workplane("XY")
               .box(120, 120, 120)
               .translate((0, 0, 60 + 60)))
cylinder = cylinder.cut(cutting_box)

# Create parabolic cavity on the inclined top surface
# Parabola: x² = 40y, or y = x²/40
# Create a profile in a 2D sketch and revolve it

# Build parabolic profile as a sketch
parabola_sketch = cq.Workplane("YZ").spline(
    [(0, 0), (5, 0.625), (10, 2.5), (15, 5.625), (20, 10), 
     (25, 15.625), (30, 22.5)],
    includeCurrent=False
)

# Close the profile to make it a closed face
parabola_profile = (cq.Workplane("YZ")
                    .moveTo(0, 0)
                    .spline([(5, -0.625), (10, -2.5), (15, -5.625), 
                            (20, -10), (25, -15.625), (30, -22.5)],
                           includeCurrent=True)
                    .lineTo(30, 0)
                    .lineTo(0, 0)
                    .close()
                    .extrude(0.1))

# Create parabolic cavity by revolving around Z-axis
cavity_sketch = (cq.Workplane("XZ")
                 .moveTo(0, 0)
                 .spline([(5, -0.625), (10, -2.5), (15, -5.625), 
                         (20, -10), (25, -15.625), (30, -22.5)],
                        includeCurrent=True)
                 .lineTo(30, 0)
                 .close())

parabolic_cavity = cavity_sketch.revolve(360, (0, 1, 0))
cylinder = cylinder.cut(parabolic_cavity)

# Create sine wave groove on cylindrical surface
# Generate 3D sine wave points
groove_points = []
num_segments = 60

for i in range(num_segments + 1):
    t = (i / num_segments) * 2 * math.pi
    x = 40.0 * math.sin(t)
    y = 40.0 * math.cos(t)
    z = 30.0 + 5.0 * math.sin(6.0 * t)
    groove_points.append((x, y, z))

# Create groove by cutting small cylindrical sections along the path
for i in range(0, len(groove_points), 3):
    pt = groove_points[i]
    # Create small cutting cylinder at each point
    small_cut = (cq.Workplane("XY")
                 .cylinder(2.0, 1.5)
                 .translate((pt[0], pt[1], pt[2])))
    try:
        cylinder = cylinder.cut(small_cut)
    except:
        pass

result = cylinder
