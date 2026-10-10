import cadquery as cq
import math

# Create a 60x60mm rectangle extruded to 100mm height
result = cq.Workplane("XY").rect(60, 60).extrude(100)

# Create a triangular cutting wedge from Z=60 at front to Z=100 at back
# Front edge (Y=30) at Z=60, back edge (Y=-30) at Z=100
cut_wedge = (
    cq.Workplane("XZ")
    .moveTo(-30, 60)
    .lineTo(30, 60)
    .lineTo(30, 100)
    .lineTo(-30, 100)
    .close()
    .extrude(60)
)

# Cut the wedge from the base
result = result.cut(cut_wedge)

# Apply shell command to create 5mm wall thickness and remove bottom
result = result.shell(5.0)

# Add a through hole (circle with diameter 20mm) on the higher rear face
# The rear face is at Y=-30 (back), drill from top
result = (
    result
    .faces(">Y")
    .workplane(origin=(0, 0, 0), invert=False)
    .center(0, 0)
    .circle(10)
    .cutThruAll()
)
