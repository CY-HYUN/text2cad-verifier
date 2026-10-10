import cadquery as cq
import math

# Create a workplane on XY to build the profile
wp = cq.Workplane("XY")

# Build the profile as a 2D sketch that will be revolved
# We'll create points for the internal and external profiles

# Internal flow path points
inlet_inner = (-20, 15)
throat = (0, 5)
outlet_inner = (80, 25)

# External profile points
inlet_outer = (-20, 20)
outlet_outer = (80, 30)

# Create parabolic points from throat to outlet
parabola_inner = []
for x in range(0, 81, 2):
    y = (1/320) * x * x + 5
    parabola_inner.append((x, y))

# Create elliptical outer profile points
ellipse_outer = []
for x in range(-20, 81, 2):
    # Smooth curve from (-20, 20) to (80, 30)
    t = (x + 20) / 100.0  # Parameter from 0 to 1
    # Elliptical interpolation
    y = 20 + (30 - 20) * t + 3 * math.sin(math.pi * t)
    ellipse_outer.append((x, y))

# Build the closed profile for revolution
profile_points = []

# Start at inlet inner point
profile_points.append(inlet_inner)

# Add arc from inlet to throat approximation
arc_points = []
for t in [i * 0.1 for i in range(11)]:
    x = inlet_inner[0] + t * (throat[0] - inlet_inner[0])
    # Circular arc approximation
    y = inlet_inner[1] + (throat[1] - inlet_inner[1]) * t - 2 * t * (1 - t)
    arc_points.append((x, y))

profile_points.extend(arc_points[1:])

# Add parabolic inner profile from throat to outlet
profile_points.extend(parabola_inner[1:])

# Connect to outlet outer
profile_points.append(outlet_outer)

# Add elliptical outer profile from outlet back to inlet
ellipse_outer_reverse = list(reversed(ellipse_outer))
profile_points.extend(ellipse_outer_reverse[1:-1])

# Connect back to inlet outer
profile_points.append(inlet_outer)

# Create a wire from these points
wire_points = [cq.Vector(p[0], 0, p[1]) for p in profile_points]
wire = cq.Wire.makePolygon(wire_points, forceWire=True)

# Create a face from the wire
face = cq.Face.makeFromWires(wire)

# Revolve the profile around the Y-axis (vertical axis through center)
result = cq.Workplane("XY").add(face).revolve(axisStart=cq.Vector(0, -50, 0), 
                                              axisEnd=cq.Vector(0, 50, 0), 
                                              angleDegrees=360)

# Add inlet flange at X=-20
inlet_flange = (
    cq.Workplane("XY")
    .circle(22)
    .extrude(5)
    .translate((0, 0, -20))
)
result = result.union(inlet_flange)

# Add outlet flange at X=80
outlet_flange = (
    cq.Workplane("XY")
    .circle(32)
    .extrude(5)
    .translate((0, 0, 80))
)
result = result.union(outlet_flange)
