import cadquery as cq
import math

# Create the main rectangular solid block
solid = cq.Workplane("XY").box(60, 60, 100, centered=True).val()

# Create a wedge to cut the top at 45 degrees
# Front (Y=-30) should be at height 60mm, rear (Y=+30) at height 100mm
# In centered coordinates: front at Z=10, rear at Z=50
wedge = cq.Workplane("XY").box(80, 80, 40, centered=True)
wedge = wedge.translate((0, 15, 30))
solid = solid.cut(wedge)

# Create hollow interior with 5mm walls
# Inner box dimensions: (60-10) x (60-10) x 100 = 50 x 50 x 100
inner_hollow = cq.Workplane("XY").box(50, 50, 100, centered=True).val()
solid = solid.cut(inner_hollow)

# Drill 20mm diameter hole in the rear wall
# Rear wall is at Y=30, drill from back
hole_radius = 10  # 20mm diameter
hole = cq.Workplane("YZ").circle(hole_radius).extrude(15, both=False).val()
hole = hole.translate((0, 30, 20))
solid = solid.cut(hole)

result = solid
