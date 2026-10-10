import cadquery as cq
import math

# Initialize with XY plane
wp = cq.Workplane("XY")

# Create a sketch on the XY plane
sketch = wp.sketch()

# Draw construction line at Y=75 (rotation axis)
sketch.geometry.addConstructionGeometry(
    sketch.geometry.makeLine(cq.Vector(-100, 75, 0), cq.Vector(300, 75, 0))
)

# Define parabola parameters
# Vertex at (100, 75), focus at (150, 75)
# For parabola: (y-k)^2 = 4p(x-h) where (h,k) is vertex and p is focal parameter
# Here: p = 50, so (y-75)^2 = 200(x-100)
# Rearranging: x = 100 + (y-75)^2/200

# Generate parabolic arc points
# We need points from where the parabola intersects x=200 back to vertex
# At x=200: (y-75)^2 = 200(200-100) = 20000, so y-75 = ±141.42, y = 75±141.42
# So y ranges from approximately -66.42 to 216.42

parabola_points = []
# Start from vertex (100, 75) and go to x=200
for y in range(-67, 217, 5):
    x = 100 + (y - 75) ** 2 / 200.0
    if x <= 200:  # Only include points up to x=200
        parabola_points.append((x, y))

# If we don't have enough points near the boundaries, add them precisely
if len(parabola_points) == 0 or parabola_points[0][0] < 100:
    parabola_points = [(100, 75)]  # Start at vertex

# Add more precise points along the parabola
precise_points = [(100.0, 75.0)]
for y in range(75, 217, 2):
    x = 100 + (y - 75) ** 2 / 200.0
    if x <= 200:
        precise_points.append((x, y))

for y in range(73, 0, -2):
    x = 100 + (y - 75) ** 2 / 200.0
    if x <= 200:
        precise_points.append((x, y))

# Remove duplicates and sort
precise_points = sorted(list(set(precise_points)))

# Draw the parabolic profile using a series of line segments
if len(precise_points) > 1:
    sketch.polyline(precise_points, forConstruction=False)

# Finalize sketch
sketch.finalize()

# Create a wire from the sketch edges (excluding construction geometry)
wire = sketch.val().edges().objects[0] if sketch.val().edges().objects else None

# Alternative approach: Create the parabola directly using cadquery geometry
# Reset and create parabolic profile manually
result = cq.Workplane("XY")

# Create points for the parabola
parabola_profile = []
for y in range(-66, 217):
    x = 100 + (y - 75) ** 2 / 200.0
    if x <= 200.01:  # Allow small tolerance for x=200
        parabola_profile.append(cq.Vector(x, y, 0))

if len(parabola_profile) > 1:
    # Create edge from parabola points
    edge = cq.Edge.makeSpline(parabola_profile)
    
    # Create wire from edge
    wire = cq.Wire.assembleEdges([edge])
    
    # Create a face from wire and revolve
    # For revolution, we need to use the right approach
    face = cq.Face.makeFromWires(wire)
    
    # Revolve around the axis at Y=75 (horizontal axis)
    # The axis direction is along X-axis, passing through (0, 75, 0)
    result = (
        cq.Workplane("XY")
        .copyWorkplane(cq.Workplane("YZ").val().plane)
        .moveTo(0, 75)
        .spline([(p.x, p.y) for p in parabola_profile])
        .close()
        .revolve(360, axisStart=(0, 75, 0), axisEnd=(1, 75, 0))
    )
else:
    # Fallback: create using revolve of a simple parabolic edge
    result = cq.Workplane("XY").center(0, 75).spline(
        [(p.x - 100, p.y - 75) for p in parabola_profile]
    ).revolve(360, (0, 1, 0))

result = cq.Workplane("XY").spline([(p.x, p.y) for p in parabola_profile]).revolve(
    360, axisStart=(0, 75, 0), axisEnd=(100, 75, 0)
)
