import cadquery as cq
import math

f = 50.0
k = 4 * f  # r^2 = k * x
depth = 100.0
t = 3.0
R = math.sqrt(k * depth)
n = 40

inner = [(depth * i / n, math.sqrt(k * depth * i / n)) for i in range(n + 1)]
outer = [(x - t, r) for (x, r) in inner]

wp = cq.Workplane("XY").moveTo(0, 0)
wp = wp.spline(inner[1:], includeCurrent=True)
wp = wp.lineTo(outer[-1][0], outer[-1][1])
wp = wp.spline(list(reversed(outer))[1:], includeCurrent=True)
wp = wp.close()

body = wp.revolve(360, (0, 0, 0), (1, 0, 0))
result = body.translate((100, 75, 0))
