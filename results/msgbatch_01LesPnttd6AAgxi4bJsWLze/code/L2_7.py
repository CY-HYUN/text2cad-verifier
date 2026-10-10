import cadquery as cq
import math

# Create the ring
ring_outer_diameter = 60
ring_inner_diameter = 30
ring_thickness = 15

# Create the ring as a cylinder with a hole
ring = cq.Workplane("XY").cylinder(ring_thickness, ring_outer_diameter/2, centered=True)
ring = ring.faces(">Z").workplane().hole(ring_inner_diameter)

# Create the rectangular rod extending radially from the ring
rod_length = 80
rod_width = 20  # cross-section width
rod_height = 15  # cross-section height

# The rod extends from the outer edge of the ring
# Position the rod so it extends radially outward from the ring
# Rod starts at the ring's outer radius and extends outward
rod_start_x = ring_outer_diameter / 2
rod_end_x = rod_start_x + rod_length

# Create the rectangular rod
rod = cq.Workplane("XY").box(rod_length, rod_width, rod_height, centered=True)
# Move the rod so it extends from the outer edge of the ring
rod = rod.translate((rod_start_x + rod_length/2, 0, 0))

# Combine ring and rod
result = ring.union(rod)

# Create the through-hole at the end of the rod
hole_diameter = 10
hole_x = rod_end_x  # At the end of the rod
hole_y = 0
hole_z = 0

# Create a cylinder for the hole (will be cut from the result)
hole_cylinder = cq.Workplane("XY").cylinder(ring_thickness + rod_height + 10, hole_diameter/2, centered=True)
hole_cylinder = hole_cylinder.translate((hole_x, hole_y, hole_z))

# Cut the hole from the rod
result = result.cut(hole_cylinder)

# Create the offset inner hole of the ring (offset by 5mm towards the rod)
offset_distance = 5
inner_hole = cq.Workplane("XY").cylinder(ring_thickness + 10, ring_inner_diameter/2, centered=True)
inner_hole = inner_hole.translate((offset_distance, 0, 0))

# Cut the offset inner hole from the ring
result = result.cut(inner_hole)

