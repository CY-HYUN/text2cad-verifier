import cadquery as cq
import math

R = 15.0      # capsule radius
L = 60.0      # straight section length
h = L / 2.0
d = R * math.cos(math.radians(45))

# Half cross-section in XZ plane (local x -> global X, local y -> global Z)
profile = (
    cq.Workplane("XZ")
    .moveTo(-h - R, 0)
    .threePointArc((-h - d, d), (-h, R))
    .lineTo(h, R)
    .threePointArc((h + d, d), (h + R, 0))
    .close()
)

# Revolve 360 degrees about the X-axis
result = profile.revolve(360, (-h - R, 0, 0), (h + R, 0, 0))
