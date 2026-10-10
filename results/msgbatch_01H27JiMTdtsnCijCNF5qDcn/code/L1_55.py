import cadquery as cq
import math

# Profile in XZ plane: (x=radius, y=Z) -> workplane "XZ" local x = global X, local y = global Z
pts = [(10.0, 0), (35.0, 0), (20.0, 60), (10.0, 60)]
profile = cq.Workplane("XZ").polyline(pts).close()

# Revolve 360 deg about the Z axis (local Y axis of the XZ workplane)
body = profile.revolve(360, (0, 0, 0), (0, 1, 0))

# Chamfer the outer edge of the bottom face (circle radius 35 at Z=0)
result = body.edges(cq.selectors.BoxSelector((-36, -36, -0.1), (36, 36, 0.1))).edges(
    cq.selectors.RadiusNthSelector(1)
).chamfer(2.0)
