import cadquery as cq
import math

L = 100.0
straight = 5.0
wavelength = 10.0
cycles = 9          # 90 mm corrugated section between the two 5 mm straight ends
r_mid = 20.0
amp = 2.5
t = 2.0

n_per = 16
N = cycles * n_per
zs = [straight + i * (L - 2 * straight) / N for i in range(N + 1)]
rm = [r_mid + amp * math.sin(2 * math.pi * (z - straight) / wavelength) for z in zs]

outer = [(r + t / 2, z) for r, z in zip(rm, zs)]
inner = [(r - t / 2, z) for r, z in zip(rm, zs)]

prof = (
    cq.Workplane("XZ")
    .moveTo(r_mid - t / 2, 0)
    .lineTo(r_mid + t / 2, 0)
    .lineTo(*outer[0])
    .spline(outer[1:], includeCurrent=True)
    .lineTo(r_mid + t / 2, L)
    .lineTo(r_mid - t / 2, L)
    .lineTo(*inner[-1])
    .spline(list(reversed(inner[:-1])), includeCurrent=True)
    .lineTo(r_mid - t / 2, 0)
    .close()
)

result = prof.revolve(360, (0, 0, 0), (0, 1, 0))
