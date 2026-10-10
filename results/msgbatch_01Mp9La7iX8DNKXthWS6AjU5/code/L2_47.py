import cadquery as cq

# Dimensions
length = 100.0
wall = 5.0
r_in = 20.0
r_out = r_in + wall          # 25
flange_h = 10.0              # radial height of flange above tube outer surface
flange_w = 5.0               # axial width
ring_h = 5.0                 # radial height of retaining ring
ring_w = 5.0                 # axial width

r_fl = r_out + flange_h
r_ring = r_out + ring_h
z_mid = length / 2.0

# Profile in the front (XZ) plane: local x = radius, local y = axial (global Z)
pts = [
    (r_in, 0),
    (r_fl, 0),
    (r_fl, flange_w),
    (r_out, flange_w),
    (r_out, z_mid - ring_w / 2),
    (r_ring, z_mid - ring_w / 2),
    (r_ring, z_mid + ring_w / 2),
    (r_out, z_mid + ring_w / 2),
    (r_out, length - flange_w),
    (r_fl, length - flange_w),
    (r_fl, length),
    (r_in, length),
]

result = (
    cq.Workplane("XZ")
    .polyline(pts)
    .close()
    .revolve(360, (0, 0, 0), (0, 1, 0))
)
