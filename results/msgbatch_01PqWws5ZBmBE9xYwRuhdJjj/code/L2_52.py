import cadquery as cq
import math

# Create a 60x60mm rectangle extruded to 100mm height
base = cq.Workplane("XY").rect(60, 60).extrude(100)

# Create a cutting tool - a triangular prism
# The triangle goes from Z=60 (front edge) to Z=100 (back edge)
# Front edge at Y=30 (front of the 60mm rectangle), back edge at Y=-30 (back)
sketch = cq.Workplane("XZ").moveTo(0, 60).lineTo(0, 100).lineTo(0, 100).close()
# Create a triangular cutting plane in XZ at the front, extending to back
cut_tool = (
    cq.Workplane("XY")
    .moveTo(0, 30)  # Front edge center
    .polyline([(0, 30), (0, -30)])  # Line from front to back in Y
    .extrude(100)  # This won't work as intended
)

# Better approach: create the cutting wedge
# Wedge from Z=60 at Y=30 (front) to Z=100 at Y=-30 (back)
points = [
    (30, 60),   # Front right at Z=60
    (30, 100),  # Front right at Z=100
    (-30, 100), # Back right at Z=100
    (-30, 60),  # Back right at Z=60
]

# Create wedge by lofting
wedge = (
    cq.Workplane("XZ")
    .moveTo(30, 60).lineTo(30, 100).lineTo(-30, 100).lineTo(-30, 60).close()
    .extrude(60)  # Extrude along X axis
)

# Cut the wedge from the base (cuts the top forming a slant)
result = base.cut(
    cq.Workplane("XY")
    .box(60, 60, 40, centered=True)
    .translate((0, 0, 80))  # Position at top
)

# Create the slanted cutting surface using a plane cut
# Cut from front (Z=60 at Y=30) to back (Z=100 at Y=-30)
cutter = (
    cq.Workplane("XY")
    .moveTo(-30, -30)
    .polyline([(-30, 30), (30, 30), (30, -30), (-30, -30)])
    .close()
    .extrude(100)
)

result = (
    cq.Workplane("XY")
    .rect(60, 60)
    .extrude(100)
)

# Create triangular cutting tool - wedge from Z=60 at front to Z=100 at back
cut_wedge = (
    cq.Workplane("XZ")
    .moveTo(-30, 60)
    .lineTo(30, 60)
    .lineTo(30, 100)
    .lineTo(-30, 100)
    .close()
    .extrude(60)
    .translate((0, 0, 0))
)

result = result.cut(cut_wedge)

# Apply shell command to create 5mm wall thickness and remove bottom
result = result.shell(5.0)

# Add a through hole (circle with diameter 20mm) on the higher rear face
# The rear face is at Y=-30, and higher means near Z=100
hole = result.faces(">Y").workplane().circle(10).cutThruAll()

# Find the rear face (highest Z, back Y) and drill hole
result = (
    result
    .faces(">Y")
    .workplane()
    .circle(10)
    .cutThruAll()
)
