import cadquery as cq
import math

# Initialize the environment and create a sketch on the XY plane
wp = cq.Workplane("XY")

# Define key points
throat_point = (0, 10)
inlet_point = (-30, 25)
outlet_point = (50, 30)

# Control points for Bezier curve converging section
inlet_x, inlet_y = inlet_point
throat_x, throat_y = throat_point
ctrl1 = (inlet_x + 8, inlet_y - 2)
ctrl2 = (throat_x - 8, throat_y)

# Parabola parameters for diverging section
# y = 10 + a*(x)^2, solve for 'a' using outlet point
a = (outlet_point[1] - throat_y) / ((outlet_point[0] - throat_x) ** 2)

# Create parabolic segment points
parabola_points = []
for x in range(0, 51, 1):
    y = throat_y + a * (x ** 2)
    parabola_points.append((x, y))

# Create sketch for the nozzle cross-section
sketch = wp.sketch()

# Draw the converging section (spline from inlet to throat)
sketch.spline([inlet_point, ctrl1, ctrl2, throat_point])

# Draw the diverging section (parabolic curve from throat to outlet)
sketch.spline(parabola_points)

# Create outlet outer point (offset by 3mm radially outward)
outlet_outer = (outlet_point[0], outlet_point[1] + 3)
inlet_outer = (inlet_point[0], inlet_point[1] + 3)

# Close the profile with offset (3mm outward)
sketch.line(outlet_point, outlet_outer)
sketch.line(outlet_outer, inlet_outer)
sketch.line(inlet_outer, inlet_point)

# Finalize and close the sketch
profile = sketch.close().finalize()

# Revolve the profile 360 degrees around the X-axis to create the Laval nozzle
result = wp.revolve(360, axis=(1, 0, 0))
