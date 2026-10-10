import cadquery as cq
import math

# Create the main hollow cylindrical liner
liner_outer_diameter = 120
liner_height = 100
liner_inner_diameter = 90  # Assume some inner diameter for hollow cylinder

# Base cylinder (hollow)
result = cq.Workplane("XY").cylinder(liner_height, liner_outer_diameter/2, liner_inner_diameter/2)

# Add 15 heat dissipation fins
num_fins = 15
fin_thickness = 2
fin_outer_diameter = 160
fin_height = liner_height / (num_fins + 1)

for i in range(1, num_fins + 1):
    z_pos = (i * liner_height) / (num_fins + 1) - liner_height/2
    
    # Create annular fin (outer cylinder - inner cylinder)
    fin = (cq.Workplane("XY")
           .workplane(offset=z_pos)
           .cylinder(fin_thickness, fin_outer_diameter/2, liner_outer_diameter/2))
    
    result = result.union(fin)

# Add hemispherical combustion chamber cover at the top
hemisphere_radius = liner_outer_diameter / 2
result = result.union(
    cq.Workplane("XY")
    .workplane(offset=liner_height/2)
    .sphere(hemisphere_radius)
    .cut(cq.Workplane("XY").workplane(offset=liner_height/2 - hemisphere_radius)
         .box(liner_outer_diameter*2, liner_outer_diameter*2, hemisphere_radius*2))
)

# Add spark plug hole at center of hemisphere (14mm diameter)
spark_plug_hole = (cq.Workplane("XY")
                   .workplane(offset=liner_height/2)
                   .cylinder(hemisphere_radius + 10, 7, 0))
result = result.cut(spark_plug_hole)

# Add intake port (oblique pipe on one side)
intake_port = (cq.Workplane("XY")
               .workplane(offset=liner_height/2 + 20)
               .transformed(offsets=(liner_outer_diameter/2 + 15, 0, 0))
               .rotated((-45, 0, 0))
               .cylinder(40, 8, 0))
result = result.cut(intake_port)

# Add exhaust port (oblique pipe on opposite side)
exhaust_port = (cq.Workplane("XY")
                .workplane(offset=liner_height/2 + 20)
                .transformed(offsets=(-(liner_outer_diameter/2 + 15), 0, 0))
                .rotated((45, 0, 0))
                .cylinder(40, 8, 0))
result = result.cut(exhaust_port)

# Add four bolt holes at the bottom at quadrant points
bolt_hole_radius = 5
bolt_positions = [
    (liner_outer_diameter/2 - 15, 0),
    (-liner_outer_diameter/2 + 15, 0),
    (0, liner_outer_diameter/2 - 15),
    (0, -liner_outer_diameter/2 + 15)
]

for x, y in bolt_positions:
    bolt_hole = (cq.Workplane("XY")
                 .workplane(offset=-liner_height/2)
                 .transformed(offsets=(x, y, 0))
                 .cylinder(liner_height + 50, bolt_hole_radius, 0))
    result = result.cut(bolt_hole)

result = result.val()
