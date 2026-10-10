import cadquery as cq
import math

f = 50.0
vx, vy = 100.0, 75.0
depth = 100.0
t = 2.0  # shell thickness behind reflective surface

R_in = math.sqrt(4 * f * depth)          # ~141.42 at X=200
R_out = math.sqrt(4 * f * (depth + t))   # outer (back) surface radius at X=200

N = 40
inner = []
for i in range(N + 1):
    r = R_in * i / N
    inner.append((vx + r * r / (4 * f), vy + r))

outer = []
for i in range(N, -1, -1):
    r = R_out * i / N
    outer.append((vx - t + r * r / (4 * f), vy + r))

profile = (
    cq.Workplane("XY")
    .moveTo(*inner[0])
    .spline(inner[1:], includeCurrent=True)
    .lineTo(*outer[0])
    .spline(outer[1:], includeCurrent=True)
    .close()
)

result = profile.revolve(360, (0, vy, 0), (1, vy, 0))
