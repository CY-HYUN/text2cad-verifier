import cadquery as cq
import math

# Create the main hollow cylindrical liner
liner_outer_diameter = 120
liner_height = 100
liner_inner_diameter = 90

# Base cylinder (hollow)
result = cq.Workplane("XY").cylinder(liner_height, liner_outer_diameter/2, liner_inner_diameter/2)

# Add 15 heat dissipation fins
num_fins = 15
fin_thickness = 2
fin_outer_diameter = 160

for i in range(1, num_fins + 1):
    z_pos = (i * liner_height) / (num_fins + 1) - liner_height/2
    
    # Create annular fin
    fin = (cq.Workplane("XY")
           .workplane(offset=z_pos)
           .cylinder(fin_thickness, fin_outer_diameter/2, liner_outer_diameter/2))
    
    result = result.union(fin)

# Add hemispherical combustion chamber cover at the top
hemisphere_radius = liner_outer_diameter / 2

# Create hemisphere by cutting a sphere
hemisphere = (cq.Workplane("XY")
              .workplane(offset=liner_height/2)
              .sphere(hemisphere_radius)
              .cut(cq.Workplane("XY")
                   .workplane(offset=liner_height/2 - hemisphere_radius)
                   .box(liner_outer_diameter * 3, liner_outer_diameter * 3, hemisphere_radius * 2)))

result = result.union(hemisphere)

# Add spark plug hole at center of hemisphere
spark_plug_hole = (cq.Workplane("XY")
                   .workplane(offset=liner_height/2)
                   .cylinder(hemisphere_radius + 10, 7, 0))
result = result.cut(spark_plug_hole)

# Add intake port
intake_base = cq.Workplane("XY").workplane(offset=liner_height/2 + 15)
intake_port = intake_base.transformed(offsets=(liner_outer_diameter/2 + 15, 0, 0))
intake_port = intake_port.cylinder(35, 8, 0)
result = result.cut(intake_port)

# Add exhaust port
exhaust_base = cq.Workplane("XY").workplane(offset=liner_height/2 + 15)
exhaust_port = exhaust_base.transformed(offsets=(-(liner_outer_diameter/2 + 15), 0, 0))
exhaust_port = exhaust_port.cylinder(35, 8, 0)
result = result.cut(exhaust_port)

# Add four bolt holes at the bottom at quadrant points
bolt_hole_radius = 5
bolt_positions = [
    (liner_outer_diameter/2 - 15, 0, 0),
    (-(liner_outer_diameter/2 - 15), 0, 0),
    (0, liner_outer_diameter/2 - 15, 0),
    (0, -(liner_outer_diameter/2 - 15), 0)
]

for pos in bolt_positions:
    bolt_hole = (cq.Workplane("XY")
                 .workplane(offset=-liner_height/2)
                 .transformed(offsets=pos)
                 .cylinder(liner_height + 50, bolt_hole_radius, 0))
    result = result.cut(bolt_hole)

result = result.val()
