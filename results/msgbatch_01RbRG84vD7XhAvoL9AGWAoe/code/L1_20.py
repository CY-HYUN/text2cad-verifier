import cadquery as cq

L = 80.0   # length along X
W = 40.0   # width along Y
H_rear = 30.0
H_front = 5.0

# Right trapezoid profile in XZ plane, extruded along Y
pts = [
    (0, 0),
    (L, 0),
    (L, H_front),
    (0, H_rear),
]

result = (
    cq.Workplane("XZ")
    .polyline(pts)
    .close()
    .extrude(-W)  # XZ normal is -Y; negative extrude goes +Y
    .translate((-L / 2, -W / 2, 0))
)
