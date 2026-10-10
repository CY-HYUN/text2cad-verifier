import cadquery as cq

outer = 60.0
wall = 3.0
inner_cav = outer - 2 * wall
core = 20.0
rod_d = 2.0
rod_len = inner_cav + wall  # extends into walls on both sides for solid union

# Hollow outer shell
shell = cq.Workplane("XY").box(outer, outer, outer).cut(
    cq.Workplane("XY").box(inner_cav, inner_cav, inner_cav)
)

# Central core cube
core_cube = cq.Workplane("XY").box(core, core, core)

# Rods along X, Y, Z axes connecting core faces to shell walls
rod_z = cq.Workplane("XY").circle(rod_d / 2).extrude(rod_len / 2, both=True)
rod_x = cq.Workplane("YZ").circle(rod_d / 2).extrude(rod_len / 2, both=True)
rod_y = cq.Workplane("XZ").circle(rod_d / 2).extrude(rod_len / 2, both=True)

result = shell.union(core_cube).union(rod_x).union(rod_y).union(rod_z)
