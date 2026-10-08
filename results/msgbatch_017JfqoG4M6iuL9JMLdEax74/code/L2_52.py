import cadquery as cq

W = 60.0      # footprint width/depth
H_rear = 100.0
H_front = 60.0
t = 5.0
hole_d = 20.0

# Side profile in YZ plane (local x = Y, local y = Z), extruded symmetrically along X
outer = (
    cq.Workplane("YZ")
    .polyline([(-W / 2, 0), (W / 2, 0), (W / 2, H_rear), (-W / 2, H_front)])
    .close()
    .extrude(W / 2, both=True)
)

# Hollow through from top to bottom
inner = cq.Workplane("XY").box(W - 2 * t, W - 2 * t, 400).translate((0, 0, 100))
shell = outer.cut(inner)

# Hole in the higher rear wall (at y = +W/2)
hole = (
    cq.Workplane("XZ", origin=(0, W / 2 + 5, 0))
    .center(0, 65)
    .circle(hole_d / 2)
    .extrude(t + 10)
)
result = shell.cut(hole)
