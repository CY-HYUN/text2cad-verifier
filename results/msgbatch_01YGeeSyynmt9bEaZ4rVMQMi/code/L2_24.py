import cadquery as cq
import math

R_out = 20.0      # outer radius (rectangle width 20)
H = 60.0          # height
r_sph = 15.0      # spherical cavity radius
r_pass = 2.5      # passage half-width (5 mm wide)
zc = 30.0         # sphere center height

z_join = zc + math.sqrt(r_sph**2 - r_pass**2)

profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(R_out, 0)
    .lineTo(R_out, H)
    .lineTo(r_pass, H)
    .lineTo(r_pass, z_join)
    .threePointArc((r_sph, zc), (0, zc - r_sph))
    .close()
)

result = profile.revolve(360, (0, 0, 0), (0, 1, 0))
