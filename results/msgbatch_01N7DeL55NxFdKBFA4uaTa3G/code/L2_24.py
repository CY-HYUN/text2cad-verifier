import cadquery as cq
import math

R_out = 20.0   # outer half-width (radius)
H = 60.0       # height
r_sph = 15.0   # cavity radius
zc = 30.0      # cavity centre height
w_half = 2.5   # half of 5 mm passage

z_join = zc + math.sqrt(r_sph**2 - w_half**2)

profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(R_out, 0)
    .lineTo(R_out, H)
    .lineTo(w_half, H)
    .lineTo(w_half, z_join)
    .threePointArc((r_sph, zc), (0, zc - r_sph))
    .close()
)

result = profile.revolve(360, (0, 0, 0), (0, 1, 0))
