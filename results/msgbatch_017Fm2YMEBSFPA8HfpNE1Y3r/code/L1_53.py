import cadquery as cq
import math

# Create a new workplane
wp = cq.Workplane("XY")

# Create the ellipse sketch in the XY plane
sketch1 = wp.sketch()
# Draw ellipse with major axis 80.0 and minor axis 50.0, centered at origin
sketch1.ellipse(80.0, 50.0)
sketch1.constrain("CenterX", "=", 0)
sketch1.constrain("CenterY", "=", 0)
sketch1 = sketch1.finalize()

# Exit sketch and extrude to create elliptical cylinder
part = sketch1.extrude(25.0)

# Get the top face for the next sketch
top_face = part.faces(">Z").first()

# Create sketch on top face
sketch2 = part.sketch(top_face)
# Draw circle at point (10.0, 0.0) with diameter 16.0 (radius 8.0)
sketch2.circle(8.0, (10.0, 0.0))
# Add horizontal dimension constraint for the 10.0 offset
sketch2.constrain("DistanceX", (10.0, 0.0), "=", 10.0)
sketch2 = sketch2.finalize()

# Perform cut-through (cut all the way through)
part = sketch2.cutThruAll()

# Apply 45-degree chamfer to the outer edge of the top face ellipse with distance 0.8
# Get the top face and its outer ellipse edges
top_face = part.faces(">Z").first()
ellipse_edges = top_face.edges()

# Apply chamfer to outer ellipse edges
part = part.chamfer(0.8, ellipse_edges)

result = part
