import cadquery as cq
import math

# Initialize the environment
wp = cq.Workplane("XY")

# Create a sketch on the XY plane (Front plane equivalent)
sketch = wp.sketch()

# Draw construction centerline along X-axis
sketch.centerline("H", (0, 0), (100, 0))

# Define key points
throat_point = (0, 10)
inlet_point = (-30, 25)
outlet_point = (50, 30)

# Create the inner wall profile using two sections

# Section 1: Converging section - Bezier spline from inlet to throat
# Start at inlet point
sketch.point(inlet_point)
sketch.point(throat_point)

# Use a spline for the converging section
# Control points for Bezier curve: inlet, control1, control2, throat
# Tangent at throat should be horizontal
# Tangent at inlet should be slightly inward
inlet_x, inlet_y = inlet_point
throat_x, throat_y = throat_point

# Control points to achieve desired tangent directions
ctrl1 = (inlet_x + 8, inlet_y - 2)  # Slightly inward tangent at inlet
ctrl2 = (throat_x - 8, throat_y)    # Horizontal tangent at throat

# Draw spline for converging section
sketch.spline(
    [inlet_point, ctrl1, ctrl2, throat_point]
)

# Section 2: Diverging section - Parabolic curve from throat to outlet
# Parabola: vertex at (0, 10), opens to the right
# General form: y = 10 + a*(x-0)^2, where we solve for 'a' using outlet point
# At x=50, y=30: 30 = 10 + a*50^2 => a = 20/2500 = 0.008
a = (outlet_point[1] - throat_y) / ((outlet_point[0] - throat_x) ** 2)

# Create parabolic segment points
parabola_points = []
for x in range(0, 51, 2):
    y = throat_y + a * (x ** 2)
    parabola_points.append((x, y))

# Draw parabolic curve
sketch.spline(parabola_points)

# Close the profile by drawing straight lines at the ends
sketch.line(outlet_point, (outlet_point[0], outlet_point[1] + 3))  # Outlet port
sketch.line((outlet_point[0], outlet_point[1] + 3), (inlet_point[0], inlet_point[1] + 3))  # Back
sketch.line((inlet_point[0], inlet_point[1] + 3), inlet_point)  # Inlet port

# Close the last segment
sketch.close()

# Offset the profile outward by 3.0mm
profile = sketch.finalize()
offset_profile = profile.offset(3.0)

# Create a new workplane with the offset profile for revolution
wp = cq.Workplane("XY")

# Draw the converging section inner profile
inner_sketch = wp.sketch()

# Draw inner profile (converging + diverging)
inner_sketch.spline([inlet_point, ctrl1, ctrl2, throat_point])
inner_sketch.spline(parabola_points)

# Draw outer profile (offset by 3mm)
outlet_outer = (outlet_point[0], outlet_point[1] + 3)
inlet_outer = (inlet_point[0], inlet_point[1] + 3)

inner_sketch.line(outlet_point, outlet_outer)
inner_sketch.line(outlet_outer, inlet_outer)
inner_sketch.line(inlet_outer, inlet_point)

inner_sketch.close()
inner_profile = inner_sketch.finalize()

# Create the Laval nozzle by revolving the profile around the X-axis
result = wp.sketch().spline([inlet_point, ctrl1, ctrl2, throat_point]).spline(parabola_points).close().finalize().revolve(360, (1, 0, 0))

# Alternative approach using a proper revolved boss
wp_final = cq.Workplane("XY")

# Create sketch for revolution
sketch_final = wp_final.sketch()

# Inner converging section
sketch_final.spline([inlet_point, ctrl1, ctrl2, throat_point])

# Inner diverging section
sketch_final.spline(parabola_points)

# Outer profile (offset)
sketch_final.line(outlet_point, outlet_outer)
sketch_final.line(outlet_outer, inlet_outer)
sketch_final.line(inlet_outer, inlet_point)

# Create closed profile
profile_final = sketch_final.close().finalize()

# Revolve around X-axis (using axis vector (1,0,0) and center point)
result = wp_final.revolve(360, axis=(1, 0, 0))
