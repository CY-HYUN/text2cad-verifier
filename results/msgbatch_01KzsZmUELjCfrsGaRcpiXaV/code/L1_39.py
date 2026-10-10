import cadquery as cq

# The plate should be 10mm thick (Z-axis), 40mm wide (Y-axis)
# Left side: rectangular prism 60mm long (X-axis), 40mm wide (Y-axis), 10mm thick (Z-axis)
# Right side: half-cylinder with 40mm diameter (20mm radius), 40mm long (Y-axis), 10mm thick (Z-axis)

# Create the rectangular prism part (60mm long x 40mm wide x 10mm thick)
# Position it so it goes from X=0 to X=60
rect_prism = cq.Workplane("XY").box(60, 40, 10)
rect_prism = rect_prism.translate((-30, 0, 0))  # Center it at origin in Y and Z

# Create a half-cylinder with radius 20mm and length 40mm (along Y-axis)
# The half-cylinder should have its flat face on the XY plane (bottom)
# Create by revolving a rectangle around the Y-axis
half_cylinder = (cq.Workplane("XZ")
                 .moveTo(20, 0)
                 .lineTo(20, 10)
                 .lineTo(0, 10)
                 .lineTo(0, 0)
                 .close()
                 .revolve(360, axisStart=(0, 0, 0), axisEnd=(0, 1, 0)))

# The half-cylinder needs to be 40mm long in Y direction
# Scale it to the correct Y length
half_cylinder = half_cylinder.translate((0, 0, -5))  # Move down so flat face is at Z=0

# Position the half-cylinder to the right of the rectangular prism (at X=60)
# The cylinder's axis should align with the Y-axis
half_cylinder = half_cylinder.translate((60, 0, 0))

# Union the two parts
result = rect_prism.union(half_cylinder)
