import cadquery as cq
import math

# Create the elliptical cylinder base by drawing an ellipse in the XY plane
# Major axis 80mm (X direction), minor axis 50mm (Y direction)
ellipse_points = []
for i in range(361):
    angle = math.radians(i)
    x = 40 * math.cos(angle)  # semi-major axis = 80/2 = 40
    y = 25 * math.sin(angle)  # semi-minor axis = 50/2 = 25
    ellipse_points.append((x, y))

# Create workplane and draw the ellipse using a spline
wp = cq.Workplane("XY")
ellipse_wire = wp.spline(ellipse_points, makeWire=True).wire()

# Create face from the ellipse wire and extrude it
body = cq.Workplane("XY").add(ellipse_wire).extrude(25)

# Create the through-hole
# Hole diameter is 16mm (radius 8mm), centered at (10, 0)
hole = cq.Workplane("XY").moveTo(10, 0).circle(8).extrude(25)

# Subtract the hole from the body
body = body.cut(hole)

# Add chamfer to the top outer edge
# Select the outer edge of the top face and chamfer it
top_edges = body.faces(">Z").edges()
body = body.chamfer(0.8, top_edges)

result = body
