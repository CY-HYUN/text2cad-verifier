import cadquery as cq
import math

# Create a sketch on the XZ plane
sketch = cq.Sketch()

# Draw the central axis (Y=0 line from X=-20 to X=80)
sketch.segment((-20, 0), (80, 0))

# Internal flow path - Arc from inlet to throat
# Inlet: X=-20, Y=15 (in XY plane, but we're in XZ, so using Y as vertical)
# Throat: X=0, Y=5
# Create arc approximation
inlet_inner = (-20, 15)
throat = (0, 5)
# Using three-point arc
sketch.arc(inlet_inner, (throat[0]-10, (inlet_inner[1]+throat[1])/2), throat)

# Parabolic segment from throat to outlet
# Parabola: vertex at (0, 5), passes through (80, 25)
# Form: y = a(x-0)^2 + 5, where 25 = a*80^2 + 5
# a = 20/6400 = 1/320
# Generate parabolic path with line segments
parabola_points = []
for x in range(0, 81, 5):
    y = (1/320) * x * x + 5
    parabola_points.append((x, y))

for i in range(len(parabola_points)-1):
    sketch.segment(parabola_points[i], parabola_points[i+1])

# External profile - elliptical arc from inlet outer to outlet outer
# Inlet outer: X=-20, Y=20
# Outlet outer: X=80, Y=30
inlet_outer = (-20, 20)
outlet_outer = (80, 30)
# Using three-point arc for elliptical approximation
mid_x = (inlet_outer[0] + outlet_outer[0]) / 2
mid_y = max(inlet_outer[1], outlet_outer[1]) + 5  # Arc bulges outward
sketch.arc(inlet_outer, (mid_x, mid_y), outlet_outer)

# Connect the profiles to form closed region
# Outlet: connect outer to inner
sketch.segment(outlet_outer, parabola_points[-1])

# Inlet: connect inner to outer
sketch.segment(inlet_inner, inlet_outer)

# Complete the sketch
sketch.close()

# Create the base workplane
wp = cq.Workplane("XZ")

# Add the sketch to the workplane
wp = wp.add(sketch)

# Revolve the profile around the Y-axis (central axis) 360 degrees
# In CadQuery, we revolve around an axis defined by a line
profile = sketch.finalize()
result = wp.revolve(axisStart=(0, 0, 0), axisEnd=(0, 1, 0), angleDegrees=360)

# Add inlet flange at X=-20
# Create a disk with radius based on inlet outer diameter
inlet_radius = 20  # Y=20 from center
inlet_flange = (
    cq.Workplane("XZ")
    .circle(inlet_radius)
    .extrude(5)  # Flange thickness
    .translate((0, 0, -20))  # Position at inlet (X=-20)
)
result = result.union(inlet_flange)

# Add outlet flange at X=80
# Create a disk with radius based on outlet outer diameter
outlet_radius = 30  # Y=30 from center
outlet_flange = (
    cq.Workplane("XZ")
    .circle(outlet_radius)
    .extrude(5)  # Flange thickness
    .translate((0, 0, 80))  # Position at outlet (X=80)
)
result = result.union(outlet_flange)

# The result is the complete revolved flow passage with flanges
result = result
