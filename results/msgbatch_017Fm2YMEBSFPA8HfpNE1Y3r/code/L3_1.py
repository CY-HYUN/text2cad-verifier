import cadquery as cq
import math

# Create parabolic profile points
# Parabola: vertex at (100, 75), focus at (150, 75)
# Formula: (y-75)^2 = 200(x-100), so x = 100 + (y-75)^2/200

parabola_points = []

# Generate points along the parabola from y=-66.42 to y=216.42 (where x=200)
for y in range(-70, 220):
    x = 100.0 + (y - 75.0) ** 2 / 200.0
    if x <= 200.01:  # Truncate at x=200
        parabola_points.append((x, y))

# Create a 3D profile by converting 2D points to 3D vectors
profile_3d = [cq.Vector(x, y, 0) for x, y in parabola_points]

# Create a spline through the parabola points
edge = cq.Edge.makeSpline(profile_3d)

# Create a wire from the edge
wire = cq.Wire.assembleEdges([edge])

# Create a face from the wire
face = cq.Face.makeFromWires(wire)

# Revolve the face around the axis at Y=75 (horizontal axis along X direction)
# Axis passes through (0, 75, 0) in direction (1, 0, 0)
result = face.revolve(
    angle=360,
    axisStart=cq.Vector(0, 75, 0),
    axisEnd=cq.Vector(1, 75, 0)
)
