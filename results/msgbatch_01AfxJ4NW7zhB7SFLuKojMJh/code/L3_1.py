import cadquery as cq
import math

f4 = 200.0
t = 2.0
H = 100.0
n = 30

outer = [(H * i / n, math.sqrt(f4 * H * i / n)) for i in range(n + 1)]
inner = [(t + (H - t) * i / n, math.sqrt(f4 * (H - t) * i / n)) for i in range(n + 1)]

wp = cq.Workplane("XY").moveTo(0, 0).spline(outer[1:], includeCurrent=True)
wp = wp.lineTo(inner[-1][0], inner[-1][1])
wp = wp.spline(list(reversed(inner))[1:], includeCurrent=True)
wp = wp.close()

shell = wp.revolve(360, (0, 0, 0), (1, 0, 0))
result = shell.translate((100, 75, 0))
