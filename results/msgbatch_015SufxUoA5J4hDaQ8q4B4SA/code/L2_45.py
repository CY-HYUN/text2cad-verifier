import cadquery as cq
import math

L = 100.0
straight = 5.0
wavelength = 10.0
cycles = 9          # 90 mm corrugated section between the two 5 mm straight ends
r_mid = 20.0        # mean outer radius (40 mm mean diameter)
amp = 2.5           # outer surface: peak dia 45, trough dia 35
t = 2.0

n_per = 16
N = cycles * n_per
zs = [straight + i * (L - 2 * straight) / N for i in range(N + 1)]
ro = [r_mid + amp * math.sin(2 * math.pi * (z - straight) / wavelength) for z in zs]

outer = [(r, z) for r, z in zip(ro, zs)]
inner = [(r - t, z) for r, z in zip(ro, zs)]

prof = (
    cq.Workplane("XZ")
    .moveTo(r_mid - t, 0)
    .lineTo(r_mid, 0)
    .lineTo(*outer[0])
    .spline(outer[1:], includeCurrent=True)
    .lineTo(r_mid, L)
    .lineTo(r_mid - t, L)
    .lineTo(*inner[-1])
    .spline(list(reversed(inner[:-1])), includeCurrent=True)
    .lineTo(r_mid - t, 0)
    .close()
)

result = prof.revolve(360, (0, 0, 0), (0, 1, 0))
