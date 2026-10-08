import cadquery as cq

L_out = 60.0
wall = 3.0
L_in_cav = L_out - 2 * wall
L_core = 20.0
rod_d = 2.0
rod_len = L_in_cav + wall  # extends into walls for a solid union

# Hollow outer shell
shell = cq.Workplane("XY").box(L_out, L_out, L_out).cut(
    cq.Workplane("XY").box(L_in_cav, L_in_cav, L_in_cav)
)

# Central core cube
core = cq.Workplane("XY").box(L_core, L_core, L_core)

# Rods along X, Y, Z through the center connecting core faces to inner walls
rod_z = cq.Workplane("XY").cylinder(rod_len, rod_d / 2)
rod_x = cq.Workplane("YZ").cylinder(rod_len, rod_d / 2)
rod_y = cq.Workplane("XZ").cylinder(rod_len, rod_d / 2)

result = shell.union(core).union(rod_x).union(rod_y).union(rod_z)
