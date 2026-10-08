import cadquery as cq

# Overall cube, centred on the origin
size = 60.0
hole_d = 20.0
z_offset_x_hole = 5.0    # axis height of the hole along X
z_offset_y_hole = -5.0   # axis height of the hole along Y
cutter_len = size * 2    # long enough to pass fully through the cube

cube = cq.Workplane("XY").box(size, size, size)

# Through-hole along X; its axis lies in the Z = 5 plane
cyl_x = (
    cq.Workplane("YZ")
    .center(0, z_offset_x_hole)
    .circle(hole_d / 2)
    .extrude(cutter_len / 2, both=True)
)

# Through-hole along Y; its axis lies in the Z = -5 plane
cyl_y = (
    cq.Workplane("XZ")
    .center(0, z_offset_y_hole)
    .circle(hole_d / 2)
    .extrude(cutter_len / 2, both=True)
)

result = cube.cut(cyl_x).cut(cyl_y)
