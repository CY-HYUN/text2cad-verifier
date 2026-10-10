import cadquery as cq
import math

# Create the main tube
tube_outer_diameter = 30
tube_inner_diameter = 20
tube_length = 100

# Create the hollow tube
tube = cq.Workplane("XY").cylinder(tube_length, tube_outer_diameter/2, tube_inner_diameter/2)

# Create the flanges (at both ends)
flange_diameter = 50
flange_thickness = 5

# Bottom flange
bottom_flange = cq.Workplane("XY").cylinder(flange_thickness, flange_diameter/2)
bottom_flange = bottom_flange.translate((0, 0, -(tube_length/2 + flange_thickness/2)))

# Top flange
top_flange = cq.Workplane("XY").cylinder(flange_thickness, flange_diameter/2)
top_flange = top_flange.translate((0, 0, (tube_length/2 + flange_thickness/2)))

# Create the central baffle
baffle_diameter = 40
baffle_thickness = 5
baffle = cq.Workplane("XY").cylinder(baffle_thickness, baffle_diameter/2)
baffle = baffle.translate((0, 0, 0))  # Center at origin

# Create a solid cylinder for the tube outer surface
tube_solid = cq.Workplane("XY").cylinder(tube_length, tube_outer_diameter/2)

# Create the inner hole
inner_hole = cq.Workplane("XY").cylinder(tube_length, tube_inner_diameter/2)
tube_final = tube_solid.cut(inner_hole)

# Combine all components
result = tube_final.union(bottom_flange).union(top_flange).union(baffle)
