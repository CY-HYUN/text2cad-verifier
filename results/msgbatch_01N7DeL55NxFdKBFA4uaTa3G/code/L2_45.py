import cadquery as cq
import math

L = 100.0
wl = 10.0
r_mid = 20.0
amp = 2.5
t = 2.0
n = 200

outer = []
for i in range(n + 1):
    x = L * i / n
    outer.append((x, r_mid + amp * math.sin(2 * math.pi * x / wl)))
inner = [(x, y - t) for (x, y) in reversed(outer)]

prof = (
    cq.Workplane("XY")
    .moveTo(*outer[0])
    .spline(outer[1:], includeCurrent=True)
    .lineTo(*inner[0])
    .spline(inner[1:], includeCurrent=True)
    .close()
)

result = prof.revolve(360, (0, 0, 0), (1, 0, 0))
