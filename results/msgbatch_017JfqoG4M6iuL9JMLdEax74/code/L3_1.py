import cadquery as cq
import math

# Paraboloid: (y-75)^2 + z^2 = 200 (x - 100), x in [100, 200]
vx, vy = 100.0, 75.0
f = 50.0
depth = 100.0
R = math.sqrt(4 * f * depth)  # rim radius ~141.42

N = 40
pts = []
for i in range(N + 1):
    r = R * i / N
    x = vx + r * r / (4 * f)
    pts.append((x, vy + r))

# Tangents: at vertex vertical; at rim dx/dr = r/(2f)
t0 = (0.0, 1.0)
t1 = (R / (2 * f), 1.0)

profile = (
    cq.Workplane("XY")
    .spline(pts, tangents=[t0, t1], includeCurrent=False)
    .lineTo(vx + depth, vy)
    .close()
)

solid = profile.revolve(360, (vx, vy, 0), (vx + depth, vy, 0))

# Extract the curved reflective surface only
faces = [fc for fc in solid.val().Faces() if fc.geomType() != "PLANE"]
surface = cq.Shell.makeShell(faces) if len(faces) > 1 else faces[0]

result = cq.Workplane("XY").newObject([surface])
