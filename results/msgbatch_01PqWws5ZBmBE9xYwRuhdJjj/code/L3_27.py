import cadquery as cq
import math

# Create the base cube with fillets
cube = cq.Workplane("XY").box(60, 60, 60).edges().fillet(12)

# Remove central sphere to create cavity
sphere = cq.Workplane("XY").sphere(20)
base_with_cavity = cube.cut(sphere)

# Create top cylinder and square flange
top_cylinder = cq.Workplane("XY").workplane(offset=30).cylinder(30, 20)
top_flange = cq.Workplane("XY").workplane(offset=60).box(60, 60, 5)
top_assembly = top_cylinder.union(top_flange)

# Create bottom cylinder and square flange
bottom_cylinder = cq.Workplane("XY").workplane(offset=-30).cylinder(30, 20)
bottom_flange = cq.Workplane("XY").workplane(offset=-65).box(60, 60, 5)
bottom_assembly = bottom_cylinder.union(bottom_flange)

# Create front cylinder and circular flange
front_cylinder = cq.Workplane("XY").workplane(offset=0).transformed(
    offsetOrigin=(0, 30, 0)
).cylinder(25, 15, centered=False)
front_flange = cq.Workplane("XY").workplane(offset=0).transformed(
    offsetOrigin=(0, 55, 0)
).cylinder(5, 25)

# Create back cylinder and circular flange
back_cylinder = cq.Workplane("XY").workplane(offset=0).transformed(
    offsetOrigin=(0, -30, 0)
).cylinder(25, 15, centered=False)
back_flange = cq.Workplane("XY").workplane(offset=0).transformed(
    offsetOrigin=(0, -55, 0)
).cylinder(5, 25)

# Create left cylinder and circular flange
left_cylinder = cq.Workplane("XY").workplane(offset=0).transformed(
    offsetOrigin=(-30, 0, 0)
).cylinder(25, 15, centered=False)
left_flange = cq.Workplane("XY").workplane(offset=0).transformed(
    offsetOrigin=(-55, 0, 0)
).cylinder(5, 25)

# Create right cylinder and circular flange
right_cylinder = cq.Workplane("XY").workplane(offset=0).transformed(
    offsetOrigin=(30, 0, 0)
).cylinder(25, 15, centered=False)
right_flange = cq.Workplane("XY").workplane(offset=0).transformed(
    offsetOrigin=(55, 0, 0)
).cylinder(5, 25)

# Combine all cylindrical parts
cylinders_and_flanges = (top_assembly
                         .union(bottom_assembly)
                         .union(front_cylinder)
                         .union(front_flange)
                         .union(back_cylinder)
                         .union(back_flange)
                         .union(left_cylinder)
                         .union(left_flange)
                         .union(right_cylinder)
                         .union(right_flange))

# Combine with base
main_body = base_with_cavity.union(cylinders_and_flanges)

# Create through-holes from top
top_hole = cq.Workplane("XY").workplane(offset=65).hole(18, 95)

# Create through-holes from bottom
bottom_hole = cq.Workplane("XY").workplane(offset=-65).hole(18, 95)

# Create through-holes from front/back/left/right
front_hole = cq.Workplane("XY").transformed(offsetOrigin=(0, 55, 0)).hole(14, 80)
back_hole = cq.Workplane("XY").transformed(offsetOrigin=(0, -55, 0)).hole(14, 80)
left_hole = cq.Workplane("XY").transformed(offsetOrigin=(-55, 0, 0)).hole(14, 80)
right_hole = cq.Workplane("XY").transformed(offsetOrigin=(55, 0, 0)).hole(14, 80)

# Apply all holes
with_holes = (main_body
              .cut(top_hole)
              .cut(bottom_hole)
              .cut(front_hole)
              .cut(back_hole)
              .cut(left_hole)
              .cut(right_hole))

# Add bolt holes on flanges (4 per flange)
bolt_radius = 4
bolt_spacing = 20

# Top flange bolt holes
for x_offset in [-bolt_spacing/2, bolt_spacing/2]:
    for y_offset in [-bolt_spacing/2, bolt_spacing/2]:
        bolt_hole = cq.Workplane("XY").workplane(offset=62.5).transformed(
            offsetOrigin=(x_offset, y_offset, 0)
        ).hole(bolt_radius * 2, 10)
        with_holes = with_holes.cut(bolt_hole)

# Bottom flange bolt holes
for x_offset in [-bolt_spacing/2, bolt_spacing/2]:
    for y_offset in [-bolt_spacing/2, bolt_spacing/2]:
        bolt_hole = cq.Workplane("XY").workplane(offset=-62.5).transformed(
            offsetOrigin=(x_offset, y_offset, 0)
        ).hole(bolt_radius * 2, 10)
        with_holes = with_holes.cut(bolt_hole)

# Side flanges bolt holes
for offset in [-bolt_spacing/2, bolt_spacing/2]:
    # Front flange
    bolt_hole_f = cq.Workplane("XY").transformed(offsetOrigin=(0, 58, offset)).hole(bolt_radius * 2, 10)
    with_holes = with_holes.cut(bolt_hole_f)
    # Back flange
    bolt_hole_b = cq.Workplane("XY").transformed(offsetOrigin=(0, -58, offset)).hole(bolt_radius * 2, 10)
    with_holes = with_holes.cut(bolt_hole_b)
    # Left flange
    bolt_hole_l = cq.Workplane("XY").transformed(offsetOrigin=(-58, 0, offset)).hole(bolt_radius * 2, 10)
    with_holes = with_holes.cut(bolt_hole_l)
    # Right flange
    bolt_hole_r = cq.Workplane("XY").transformed(offsetOrigin=(58, 0, offset)).hole(bolt_radius * 2, 10)
    with_holes = with_holes.cut(bolt_hole_r)

# Create triangular reinforcement plates at four corners
reinforcement_plates = cq.Workplane("XY")
for x_sign in [-1, 1]:
    for y_sign in [-1, 1]:
        plate = (cq.Workplane("XY")
                .workplane(offset=25)
                .polyline([
                    (x_sign * 18, y_sign * 18, 0),
                    (x_sign * 30, y_sign * 30, 0),
                    (x_sign * 18, y_sign * 30, 0),
                    (x_sign * 18, y_sign * 18, 0)
                ])
                .close()
                .extrude(5))
        reinforcement_plates = reinforcement_plates.union(plate)

# Combine everything
result = with_holes.union(reinforcement_plates)
