import cadquery as cq

# Create outer semi-cylinder (radius 30mm, length 100mm)
outer_cylinder = cq.Workplane("XY").cylinder(height=100, radius=30, centered=True)

# Cut to make it a semi-cylinder by cutting away the bottom half
outer_semi = outer_cylinder.faces(">Z").workplane().rect(60, 100, centered=True).cutThruAll()

# Create inner semi-cylinder (radius 20mm, length 100mm)
inner_cylinder = cq.Workplane("XY").cylinder(height=100, radius=20, centered=True)

# Cut to make it a semi-cylinder
inner_semi = inner_cylinder.faces(">Z").workplane().rect(40, 100, centered=True).cutThruAll()

# Create the shell by subtracting inner from outer
# Start fresh with proper approach
outer = cq.Workplane("XY").cylinder(height=100, radius=30, centered=True)
# Cut the cylinder in half along XY plane to get semi-cylinder
outer_semi_shell = outer.cut(cq.Workplane("XY").box(60, 60, 100, centered=True).translate((0, -30, 0)))

# Create inner cylinder and cut it in half
inner = cq.Workplane("XY").cylinder(height=100, radius=20, centered=True)
inner_semi_shell = inner.cut(cq.Workplane("XY").box(40, 40, 100, centered=True).translate((0, -20, 0)))

# Subtract the inner semi-cylinder from the outer semi-cylinder
result = outer_semi_shell.cut(inner_semi_shell)
