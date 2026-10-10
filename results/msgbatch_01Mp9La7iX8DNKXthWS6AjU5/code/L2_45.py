import cadquery as cq
import math

L = 100.0
wavelength = 10.0
r_mid = 20.0
amp = 2.5
t = 2.0  # wall thickness (inward offset)

n_per = 16
N = int(L / wavelength) * n_per
xs = [L * i / N for i in range(N + 1)]
outer = [(x, r_mid + amp * math.cos(2 * math.pi * x / wavelength)) for x in xs]
inner = [(x, y - t) for x, y in outer]

wp = (
    cq.Workplane("XY")
    .moveTo(*outer[0])
    .spline(outer[1:], includeCurrent=True)
    .lineTo(*inner[-1])
    .spline(list(reversed(inner))[1:], includeCurrent=True)
    .close()
)

result = wp.revolve(360, (0, 0, 0), (1, 0, 0))
