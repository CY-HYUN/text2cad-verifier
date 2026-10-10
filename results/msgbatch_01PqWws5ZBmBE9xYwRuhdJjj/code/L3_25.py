import cadquery as cq
import math

# Create the main hollow cylinder sleeve
# Outer diameter: 120mm, Inner diameter: 100mm (assuming 10mm wall thickness), Height: 100mm
outer_diameter = 120
inner_diameter = 100
cylinder_height = 100

# Create the hollow cylinder
cylinder = cq.Workplane("XY").circle(outer_diameter / 2).extrude(cylinder_height)
cylinder = cylinder.cut(cq.Workplane("XY").circle(inner_diameter / 2).extrude(cylinder_height))

# Create the circular ring on the outer wall (at mid-height for reference)
ring_outer_diameter = 160
ring_thickness = 2
ring_inner_diameter = ring_outer_diameter - 2 * ring_thickness
ring_height = 5

# Ring positioned at mid-height of cylinder
ring = cq.Workplane("XY").circle(ring_outer_diameter / 2).extrude(ring_height)
ring = ring.cut(cq.Workplane("XY").circle(ring_inner_diameter / 2).extrude(ring_height))
ring = ring.translate((0, 0, cylinder_height / 2 - ring_height / 2))

# Create heat dissipation fins (15 layers)
num_fins = 15
fin_thickness = 1.5
fin_height = 8
fin_radius = (ring_outer_diameter / 2) + 5

fins = cq.Workplane("XY")
fin_spacing = cylinder_height / (num_fins - 1)

for i in range(num_fins):
    z_pos = i * fin_spacing
    # Create a rectangular fin extending radially
    fin = cq.Workplane("XY").box(fin_thickness, fin_radius * 2, fin_height).translate((fin_radius / 2, 0, z_pos))
    fins = fins.union(fin)

# Combine cylinder and ring
result = cylinder.union(ring)

# Add fins to the assembly
result = result.union(fins)

# Create hemispherical cover on top
hemisphere_radius = 60
hemisphere = cq.Workplane("XY").sphere(hemisphere_radius).translate((0, 0, cylinder_height + hemisphere_radius))

# Cut the upper half to make it a hemisphere
hemisphere = hemisphere.cut(cq.Workplane("XY").box(hemisphere_radius * 3, hemisphere_radius * 3, hemisphere_radius).translate((0, 0, cylinder_height)))

# Drill spark plug hole (14mm diameter) from top center
spark_plug_hole = cq.Workplane("XY").circle(7).extrude(hemisphere_radius + 10).translate((0, 0, cylinder_height))
hemisphere = hemisphere.cut(spark_plug_hole)

# Union hemisphere with main body
result = result.union(hemisphere)

# Create intake and exhaust tubular structures on hemispherical surface
intake_diameter = 20
exhaust_diameter = 20
tube_length = 30

# Intake tube (angled towards one side)
intake_tube = cq.Workplane("XY").circle(intake_diameter / 2).extrude(tube_length)
intake_tube = intake_tube.translate((35, 0, cylinder_height + hemisphere_radius - 20)).rotateAboutCenter((1, 0, 0), 20)

# Exhaust tube (angled towards opposite side)
exhaust_tube = cq.Workplane("XY").circle(exhaust_diameter / 2).extrude(tube_length)
exhaust_tube = exhaust_tube.translate((-35, 0, cylinder_height + hemisphere_radius - 20)).rotateAboutCenter((1, 0, 0), -20)

# Union intake and exhaust tubes
result = result.union(intake_tube).union(exhaust_tube)

# Create and cut four bolt holes at four quadrant points at the bottom
bolt_hole_diameter = 8
bolt_hole_radius = bolt_hole_diameter / 2
bolt_distance_from_center = 40  # Distance from center axis

# Create four bolt holes at quadrant positions
bolt_positions = [
    (bolt_distance_from_center, 0),
    (-bolt_distance_from_center, 0),
    (0, bolt_distance_from_center),
    (0, -bolt_distance_from_center)
]

for x, y in bolt_positions:
    bolt_hole = cq.Workplane("XY").circle(bolt_hole_radius).extrude(cylinder_height + hemisphere_radius + 50)
    bolt_hole = bolt_hole.translate((x, y, -25))
    result = result.cut(bolt_hole)

result = result
