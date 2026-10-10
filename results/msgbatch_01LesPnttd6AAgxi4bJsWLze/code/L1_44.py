import cadquery as cq

# Create the main cube
side_length = 40
cube = cq.Workplane("XY").box(side_length, side_length, side_length)

# Create the through-hole (diameter 20mm)
through_hole_diameter = 20
cube = cube.faces(">Z").workplane().hole(through_hole_diameter)

# Create the counterbore (diameter 30mm, depth 10mm from top)
counterbore_diameter = 30
counterbore_depth = 10
cube = cube.faces(">Z").workplane().hole(counterbore_diameter, counterbore_depth)

result = cube
