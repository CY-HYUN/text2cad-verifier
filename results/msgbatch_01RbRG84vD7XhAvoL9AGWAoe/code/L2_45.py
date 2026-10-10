import cadquery as cq
import math

L_total = 100.0
L_straight = 5.0
L_wave = L_total - 2 * L_straight
cycles = 10
lam = L_wave / cycles
r_mid = 20.0
amp = 2.5
t = 2.0

n = 200
outer = []
inner = []
for i in range(n + 1):
    z = L_straight + L_wave * i / n
    r = r_mid + amp * math.sin(2 * math.pi * (z - L_straight) / lam)
    outer.append((r + t / 2, z))
    inner.append((r - t / 2, z))

ro0 = r_mid + t / 2
ri0 = r_mid - t / 2

prof = (
    cq.Workplane("XY")
    .moveTo(ri0, 0)
    .lineTo(ro0, 0)
    .lineTo(ro0, L_straight)
    .spline(outer[1:], includeCurrent=True)
    .lineTo(ro0, L_total)
    .lineTo(ri0, L_total)
    .lineTo(ri0, L_total - L_straight)
    .spline(list(reversed(inner))[1:], includeCurrent=True)
    .close()
)

result = prof.revolve(360, (0, 0, 0), (0, 1, 0))
