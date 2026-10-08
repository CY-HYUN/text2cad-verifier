import cadquery as cq
import math

# Base plate: 100 x 50 x 3
L, W, T = 100.0, 50.0, 3.0
plate = cq.Workplane("XY").box(L, W, T, centered=(False, True, False))

# Sine band profile in the XZ plane, extruded across the 50 mm width
A = 5.0          # amplitude
period = 20.0
thk = 1.0        # band thickness
zc = T + A - 0.5  # centreline height; troughs dip 0.5 mm into the plate for a solid merge

N = 200
ts = [L * i / N for i in range(N + 1)]
upper = [(t, zc + A * math.sin(2 * math.pi * t / period)) for t in ts]
lower = [(t, zc - thk + A * math.sin(2 * math.pi * t / period)) for t in ts]

fin = (
    cq.Workplane("XZ")
    .moveTo(*lower[0])
    .spline(lower[1:], includeCurrent=True)
    .lineTo(*upper[-1])
    .spline(list(reversed(upper))[1:], includeCurrent=True)
    .close()
    .extrude(W / 2.0, both=True)
)

result = plate.union(fin)
