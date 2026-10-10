import cadquery as cq
import math

# Create the sketch on the front plane (XY plane)
sketch = (
    cq.Sketch()
    # Outer rectangle: 20mm wide, 60mm tall, centered at origin
    .rect(20, 60)
    # Inner semicircle: radius 15mm, positioned in the lower half
    # The semicircle will be at the bottom, opening upward
    .push([(0, -15)])
    .circle(15)
)

# Create a workplane on the front plane
wp = cq.Workplane("front")

# Draw the outer rectangle
outer = wp.rect(20, 60)

# Create the profile for revolution
# We need to create a 2D profile that when revolved creates the desired 3D shape
# Profile: outer rectangle (20x60), with semicircle cutout at bottom (r=15), 
# and a 5mm passage at top

profile = (
    cq.Sketch()
    # Start with the outer boundary
    # Rectangle points: bottom-left, bottom-right, top-right, top-left
    .move(10, 0)  # Move to right edge middle
    .line(0, 30)  # Go up to top right (half height)
    .line(-5, 0)  # Inward 5mm (passage width)
    .arc((0, 15), 15)  # Arc for semicircle - radius 15, centered at (0, 15)
    .line(5, 0)   # Back out 5mm
    .line(0, 30)  # Back to top
    .close()
)

# Use the profile to create a revolved solid
# Create the 2D profile as a sketch
wp_profile = cq.Workplane("XZ").center(0, 30)

# Create profile points for the revolution
# The profile should be drawn on the XZ plane, from the axis of revolution
pts = [
    (10, 0),      # Start at outer right, bottom
    (10, 30),     # Up to outer right, top
    (5, 30),      # Inward 5mm at top (passage)
    (5, 15),      # Down to semicircle start
]

# Create semicircle points (approximated with arc)
semicircle_points = []
for i in range(17):  # 0 to 16 points for semicircle
    angle = i * math.pi / 16  # 0 to pi radians
    x = 15 * math.cos(angle)
    y = 15 - 15 * math.sin(angle)  # Semicircle center at y=15
    semicircle_points.append((x, y))

# Complete the profile
profile_points = [
    (10, 0),
    (10, 30),
    (5, 30),
] + semicircle_points[::-1] + [(10, 0)]

# Create a face from the profile and revolve it
# Using a different approach: create the profile as a wire
wp_rev = cq.Workplane("XZ")
wp_rev = wp_rev.moveTo(10, 0)
wp_rev = wp_rev.lineTo(10, 30)
wp_rev = wp_rev.lineTo(5, 30)

# Draw semicircle from (5,15) to (5,15) with radius 15, center at (0,15)
for i in range(len(semicircle_points) - 1):
    x1, y1 = semicircle_points[i]
    x2, y2 = semicircle_points[i + 1]
    wp_rev = wp_rev.lineTo(x2, y2)

wp_rev = wp_rev.lineTo(10, 0)
wp_rev = wp_rev.close()

# Create a face and revolve around Z axis
face = wp_rev.val()
result = wp_rev.revolve(360, (0, 0, 1))
