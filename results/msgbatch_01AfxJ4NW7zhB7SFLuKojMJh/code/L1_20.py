import cadquery as cq

pts = [(0, 0), (80, 0), (80, 5), (0, 30)]
# Profile in the XZ plane, extruded along Y
result = (
    cq.Workplane("XZ")
    .polyline(pts)
    .close()
    .extrude(-40)  # XZ normal is -Y, so negative extrude goes toward +Y
)
