import cadquery as cq

# Dimensions
L = 100.0          # tube length
t = 5.0            # wall thickness
r_in = 20.0        # inner radius
r_out = r_in + t   # outer radius of tube body
fl_h = 10.0        # flange radial height
fl_w = 5.0         # flange axial width
ring_h = 5.0       # retaining ring radial height
ring_w = 5.0       # retaining ring axial width

zm0 = L / 2 - ring_w / 2
zm1 = L / 2 + ring_w / 2

# Closed profile in the front (XZ) plane: x = radius, local y = axial position
pts = [
    (r_in, 0),
    (r_out + fl_h, 0),
    (r_out + fl_h, fl_w),
    (r_out, fl_w),
    (r_out, zm0),
    (r_out + ring_h, zm0),
    (r_out + ring_h, zm1),
    (r_out, zm1),
    (r_out, L - fl_w),
    (r_out + fl_h, L - fl_w),
    (r_out + fl_h, L),
    (r_in, L),
]

result = (
    cq.Workplane("XZ")
    .polyline(pts)
    .close()
    .revolve(360, (0, 0, 0), (0, 1, 0))
)
