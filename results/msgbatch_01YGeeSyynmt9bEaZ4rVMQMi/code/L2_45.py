import cadquery as cq
import math

L = 100.0
wl = 10.0
r_mean = 20.0
amp = 2.5
t = 2.0
N = 400

zs = [L * i / N for i in range(N + 1)]
outer = [(r_mean + amp * math.cos(2 * math.pi * z / wl), z) for z in zs]
inner = [(r - t, z) for (r, z) in outer]

prof = (
    cq.Workplane("XZ")
    .moveTo(*outer[0])
    .spline(outer[1:], includeCurrent=True)
    .lineTo(*inner[-1])
    .spline(list(reversed(inner))[1:], includeCurrent=True)
    .close()
)

result = prof.revolve(360, (0, 0, 0), (0, 1, 0))
