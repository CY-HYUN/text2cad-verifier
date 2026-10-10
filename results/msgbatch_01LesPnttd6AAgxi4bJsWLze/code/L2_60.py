import cadquery as cq
import math

# Create the main ring body
# Outer diameter: 90mm, inner diameter: 40mm, thickness: 25mm
outer_radius = 45
inner_radius = 20
thickness = 25

# Start with a solid cylinder
result = cq.Workplane("XY").cylinder(height=thickness, radius=outer_radius)

# Cut out the inner hole
result = result.cut(cq.Workplane("XY").cylinder(height=thickness, radius=inner_radius))

# Extended feature 1: 6 radial through-holes on outer cylindrical surface
# Holes at 0, 60, 120, 180, 240, 300 degrees
# Radial holes with diameter 10mm, positioned at radius 32.5mm (middle of wall)
radial_hole_radius = (outer_radius + inner_radius) / 2  # 32.5mm from center
radial_hole_diameter = 10
radial_hole_count = 6

for i in range(radial_hole_count):
    angle = (i * 360 / radial_hole_count) * math.pi / 180
    x = radial_hole_radius * math.cos(angle)
    y = radial_hole_radius * math.sin(angle)
    
    # Create a hole that goes radially through the wall
    hole = cq.Workplane("XY").workplane(offset=0).moveTo(x, y).circle(radial_hole_diameter / 2).extrude(-thickness, combine=False)
    result = result.cut(hole)

# Extended feature 2: 6 countersunk holes on upper end face
# Holes at 30, 90, 150, 210, 270, 330 degrees
# Positioned on a circle with diameter 65mm (radius 32.5mm)
axial_hole_radius = 32.5
axial_hole_diameter = 8
axial_hole_count = 6

for i in range(axial_hole_count):
    angle = (30 + i * 360 / axial_hole_count) * math.pi / 180
    x = axial_hole_radius * math.cos(angle)
    y = axial_hole_radius * math.sin(angle)
    
    # Create countersunk hole on top face
    # Countersink depth and angle (standard 82 degree countersink, depth ~4mm for 8mm diameter)
    countersink_diameter = 8
    countersink_depth = 4
    
    # Create the hole with countersink
    hole_workplane = cq.Workplane("XY").workplane(offset=thickness).moveTo(x, y)
    
    # Countersink portion (cone)
    countersink = hole_workplane.circle(countersink_diameter / 2).cone(height=countersink_depth, 
                                                                       topRadius=0, 
                                                                       bottomRadius=countersink_diameter / 2,
                                                                       direct=(0, 0, -1))
    
    # Through hole portion
    through_hole = cq.Workplane("XY").moveTo(x, y).circle(axial_hole_diameter / 2).extrude(-thickness, combine=False)
    
    result = result.cut(through_hole)
    result = result.cut(countersink)

