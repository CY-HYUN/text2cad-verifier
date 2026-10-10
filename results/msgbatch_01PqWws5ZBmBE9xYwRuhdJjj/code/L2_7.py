import cadquery as cq
import math

# Create the main body
# Start with a circle of diameter 60mm centered at origin
sketch = cq.Sketch().circle(30)

# Add a rectangle 80mm long and 20mm wide along positive X-axis, tangent to circle
# The circle has radius 30mm, so rectangle starts at x=30 and extends to x=110
# Rectangle is 20mm wide (±10mm in Y direction)
rect_sketch = cq.Sketch().rect(80, 20, forConstruction=False).moveTo(30 + 40, 0)
sketch = sketch.union(rect_sketch)

# Extrude the sketch to create main body (15mm extrusion)
main_body = cq.Workplane("XY").placeSketch(sketch).extrude(15)

# Select the top surface and cut a circle with diameter 30mm at X=5mm
# The top surface is at Z=15
top_surface = main_body.faces(">Z").workplane()
top_surface_wp = top_surface.moveTo(5, 0)
cut1 = top_surface_wp.circle(15).cutThruAll()

# Perform the first cut (circle at x=5, diameter 30mm)
main_body = main_body.cut(cut1)

# For the second cut: at the center of the end of the connecting rod
# The rectangle extends from x=30 to x=110, so the end is at x=110
# The rectangle center in Y is at y=0
# Draw a circle with diameter 10mm (radius 5mm) at the end center and cut through
end_cut_wp = main_body.workplane(offset=0).moveTo(110, 0)
end_cut = end_cut_wp.circle(5).cutThruAll()

# Perform the second cut
main_body = main_body.cut(end_cut)

result = main_body
