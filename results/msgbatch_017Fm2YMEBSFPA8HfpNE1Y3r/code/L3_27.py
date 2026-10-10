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
front_cyl_base = cq.Workplane("XY").moveTo(0, 30).circle(15).extrude(25)
front_flange = cq.Workplane("XY").moveTo(0, 55).circle(25).extrude(5)

# Create back cylinder and circular flange
back_cyl_base = cq.Workplane("XY").moveTo(0, -30).circle(15).extrude(25)
back_flange = cq.Workplane("XY").moveTo(0, -55).circle(25).extrude(5)

# Create left cylinder and circular flange
left_cyl_base = cq.Workplane("XY").moveTo(-30, 0).circle(15).extrude(25)
left_flange = cq.Workplane("XY").moveTo(-55, 0).circle(25).extrude(5)

# Create right cylinder and circular flange
right_cyl_base = cq.Workplane("XY").moveTo(30, 0).circle(15).extrude(25)
right_flange = cq.Workplane("XY").moveTo(55, 0).circle(25).extrude(5)

# Combine all cylindrical parts
cylinders_and_flanges = (top_assembly
                         .union(bottom_assembly)
                         .union(front_cyl_base)
                         .union(front_flange)
                         .union(back_cyl_base)
                         .union(back_flange)
                         .union(left_cyl_base)
                         .union(left_flange)
                         .union(right_cyl_base)
                         .union(right_flange))

# Combine with base
main_body = base_with_cavity.union(cylinders_and_flanges)

# Create through-hole from top (cylinder through center)
top_hole = cq.Workplane("XY").circle(18).extrude(-100)
main_body = main_body.cut(top_hole)

# Create through-hole from bottom
bottom_hole = cq.Workplane("XY").circle(18).extrude(100)
main_body = main_body.cut(bottom_hole)

# Create through-hole from front
front_hole = cq.Workplane("XY").moveTo(0, 30).circle(14).extrude(-80)
main_body = main_body.cut(front_hole)

# Create through-hole from back
back_hole = cq.Workplane("XY").moveTo(0, -30).circle(14).extrude(80)
main_body = main_body.cut(back_hole)

# Create through-hole from left
left_hole = cq.Workplane("XY").moveTo(-30, 0).circle(14).extrude(-80)
main_body = main_body.cut(left_hole)

# Create through-hole from right
right_hole = cq.Workplane("XY").moveTo(30, 0).circle(14).extrude(80)
main_body = main_body.cut(right_hole)

with_holes = main_body

# Add bolt holes on top flange (4 per flange)
bolt_radius = 4
bolt_spacing = 20

# Top flange bolt holes
for x_offset in [-bolt_spacing/2, bolt_spacing/2]:
    for y_offset in [-bolt_spacing/2, bolt_spacing/2]:
        bolt_hole = cq.Workplane("XY").moveTo(x_offset, y_offset).circle(bolt_radius).extrude(-10)
        with_holes = with_holes.cut(bolt_hole)

# Bottom flange bolt holes
for x_offset in [-bolt_spacing/2, bolt_spacing/2]:
    for y_offset in [-bolt_spacing/2, bolt_spacing/2]:
        bolt_hole = cq.Workplane("XY").moveTo(x_offset, y_offset).circle(bolt_radius).extrude(10)
        with_holes = with_holes.cut(bolt_hole)

# Front flange bolt holes
for x_offset in [-bolt_spacing/2, bolt_spacing/2]:
    for z_offset in [-bolt_spacing/2, bolt_spacing/2]:
        bolt_hole = cq.Workplane("XY").moveTo(x_offset, 55).circle(bolt_radius).extrude(-5)
        with_holes = with_holes.cut(bolt_hole)

# Back flange bolt holes
for x_offset in [-bolt_spacing/2, bolt_spacing/2]:
    for z_offset in [-bolt_spacing/2, bolt_spacing/2]:
        bolt_hole = cq.Workplane("XY").moveTo(x_offset, -55).circle(bolt_radius).extrude(5)
        with_holes = with_holes.cut(bolt_hole)

# Left flange bolt holes
for y_offset in [-bolt_spacing/2, bolt_spacing/2]:
    for z_offset in [-bolt_spacing/2, bolt_spacing/2]:
        bolt_hole = cq.Workplane("XY").moveTo(-55, y_offset).circle(bolt_radius).extrude(-5)
        with_holes = with_holes.cut(bolt_hole)

# Right flange bolt holes
for y_offset in [-bolt_spacing/2, bolt_spacing/2]:
    for z_offset in [-bolt_spacing/2, bolt_spacing/2]:
        bolt_hole = cq.Workplane("XY").moveTo(55, y_offset).circle(bolt_radius).extrude(5)
        with_holes = with_holes.cut(bolt_hole)

# Create triangular reinforcement plates at four corners
reinforcements = cq.Workplane("XY")
for x_sign in [-1, 1]:
    for y_sign in [-1, 1]:
        # Create a triangular plate using polyline
        plate_pts = [
            (x_sign * 18, y_sign * 18),
            (x_sign * 30, y_sign * 30),
            (x_sign * 18, y_sign * 30)
        ]
        plate = (cq.Workplane("XY")
                .moveTo(x_sign * 18, y_sign * 18)
                .polyline([(x_sign * 30, y_sign * 30),
                          (x_sign * 18, y_sign * 30)])
                .close()
                .extrude(5)
                .translate((0, 0, 25)))
        reinforcements = reinforcements.union(plate)

# Combine everything
result = with_holes.union(reinforcements)
