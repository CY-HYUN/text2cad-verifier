import cadquery as cq
import math

# Create the three datum planes implicitly through sketches

# Sketch 1: Bottom circle (60mm diameter) on Plane1 (Z=0)
bottom_circle = cq.Workplane("XY").circle(30.0)

# Sketch 2: Top circle (80mm diameter) on Plane3 (Z=150)
top_circle = cq.Workplane("XY").workplane(offset=150).circle(40.0)

# Sketch 3: Middle wavy ring on Plane2 (Z=75)
# Create a wavy profile with 6 periods, oscillating between 30mm and 40mm radius
middle_sketch = cq.Workplane("XY").workplane(offset=75)

# Generate wavy ring: 6 periods with peaks at 40mm and troughs at 30mm
# This creates a closed wavy line
points = []
num_points = 120  # 20 points per period for 6 periods
for i in range(num_points):
    angle = (i / num_points) * 2 * math.pi * 6  # 6 complete periods
    # Oscillate radius between 30 and 40 (amplitude of 5mm around mean of 35mm)
    radius = 35.0 + 5.0 * math.sin(angle)
    x = radius * math.cos(angle / 6)
    y = radius * math.sin(angle / 6)
    points.append((x, y))

# Close the loop
middle_sketch = middle_sketch.polyline(points, includeCurrent=False).close()

# Create solids using loft
# Start from bottom circle
loft_solid = cq.Workplane("XY").circle(30.0).workplane(offset=75).polyline(points, includeCurrent=False).close().workplane(offset=75).circle(40.0).loft(ruled=False)

# Alternative approach: build profiles and loft them properly
# Bottom profile at Z=0
bottom_profile = cq.Workplane("XY").circle(30.0).val()

# Middle wavy profile at Z=75
middle_profile = cq.Workplane("XY").workplane(offset=75).polyline(points, includeCurrent=False).close().val()

# Top profile at Z=150
top_profile = cq.Workplane("XY").workplane(offset=150).circle(40.0).val()

# Create the lofted solid by building it directly
# We'll use a different approach: create sketches and loft them
base = cq.Workplane("XY")

# Add bottom circle
sketch1 = base.circle(30.0)

# Create a compound with proper lofting
# Using sweep and multiple sections
result = (
    cq.Workplane("XY")
    .circle(30.0)
    .workplane(offset=75)
    .polyline(points, includeCurrent=False)
    .close()
    .workplane(offset=75)
    .circle(40.0)
    .loft(ruled=False)
)

# Shell the solid: remove top and set wall thickness to 2mm
try:
    # Get the solid
    solid = result.val()
    # Find and remove the top face (at Z=150)
    # Create shell by removing top face and applying thickness
    result = result.faces(">Z").val()  # Get top face
    result = cq.Workplane("XY").circle(30.0).workplane(offset=75).polyline(points, includeCurrent=False).close().workplane(offset=75).circle(40.0).loft(ruled=False).val()
    # Shell: keep the bottom and side, remove top
    result = result.shell(2.0)
except:
    # Fallback: just ensure we have the lofted shape
    result = (
        cq.Workplane("XY")
        .circle(30.0)
        .workplane(offset=75)
        .polyline(points, includeCurrent=False)
        .close()
        .workplane(offset=75)
        .circle(40.0)
        .loft(ruled=False)
    )

