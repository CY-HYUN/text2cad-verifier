import cadquery as cq

outer = 60.0
wall = 5.0
inner = outer - 2 * wall  # 50
small = 20.0
rod_d = 2.0
rod_len = inner + 1.0  # slight overlap into walls for a solid merge

# Closed hollow shell (no faces removed, cavity retained)
shell = cq.Workplane("XY").box(outer, outer, outer).cut(
    cq.Workplane("XY").box(inner, inner, inner)
)

# Central small cube
core = cq.Workplane("XY").box(small, small, small)

# Rods from each face centre of the small cube to the inner shell walls
rod_z = cq.Workplane("XY").circle(rod_d / 2).extrude(rod_len / 2, both=True)
rod_x = cq.Workplane("YZ").circle(rod_d / 2).extrude(rod_len / 2, both=True)
rod_y = cq.Workplane("XZ").circle(rod_d / 2).extrude(rod_len / 2, both=True)

result = shell.union(core).union(rod_x).union(rod_y).union(rod_z)
