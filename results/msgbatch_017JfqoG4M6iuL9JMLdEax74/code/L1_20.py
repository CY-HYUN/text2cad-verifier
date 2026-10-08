import cadquery as cq

# Wedge stop: right-trapezoid profile in the XZ plane, extruded along Y
L, W = 80.0, 40.0
h_rear, h_front = 30.0, 5.0

pts = [(0, 0), (L, 0), (L, h_front), (0, h_rear)]
result = (
    cq.Workplane("XZ")
    .polyline(pts).close()
    .extrude(-W)  # XZ normal is -Y; negative extrude goes +Y
    .translate((-L / 2, -W / 2, 0))
)
