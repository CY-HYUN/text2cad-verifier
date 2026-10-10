import cadquery as cq
import math

# Create the elliptical cylinder base
# Draw an ellipse in the XY plane with major axis 80mm (X) and minor axis 50mm (Y)
ellipse_points = []
for i in range(360):
    angle = math.radians(i)
    x = 40 * math.cos(angle)  # semi-major axis = 80/2 = 40
    y = 25 * math.sin(angle)  # semi-minor axis = 50/2 = 25
    ellipse_points.append((x, y))

# Create the ellipse as a closed wire
ellipse = cq.Workplane("XY").moveTo(0, 0).spline(ellipse_points, makeWire=True)

# Extrude the ellipse 25mm in the positive Z direction
body = cq.Workplane("XY").add(ellipse).extrude(25)

# Create the through-hole
# Hole diameter is 16mm, radius is 8mm, centered at (10, 0)
hole = cq.Workplane("XY").moveTo(10, 0).circle(8).extrude(25)

# Subtract the hole from the body
body = body.cut(hole)

# Add chamfer to the top outer edge
# The chamfer is 45 degrees with width 0.8mm on the outer edge of the top ellipse
edges = body.faces(">Z").edges()
body = body.chamfer(0.8, edges)

result = body
