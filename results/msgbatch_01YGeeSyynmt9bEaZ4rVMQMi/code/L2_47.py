import cadquery as cq

# Dimensions (mm)
L = 100.0        # tube length
t = 5.0          # wall thickness
ri = 20.0        # inner radius (assumed)
ro = ri + t      # outer radius of tube body
fh = 10.0        # flange height (radial)
fw = 5.0         # flange width (axial)
rh = 5.0         # retaining ring height (radial)
rw = 5.0         # retaining ring width (axial)

zm = L / 2.0

# Half cross-section profile (r, z) in the front (XZ) plane
pts = [
    (ri, 0),
    (ro + fh, 0),
    (ro + fh, fw),
    (ro, fw),
    (ro, zm - rw / 2),
    (ro + rh, zm - rw / 2),
    (ro + rh, zm + rw / 2),
    (ro, zm + rw / 2),
    (ro, L - fw),
    (ro + fh, L - fw),
    (ro + fh, L),
    (ri, L),
]

result = (
    cq.Workplane("XZ")
    .polyline(pts)
    .close()
    .revolve(360, (0, 0, 0), (0, 1, 0))
)
