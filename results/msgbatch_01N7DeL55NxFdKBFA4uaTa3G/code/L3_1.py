import cadquery as cq
import math

# Parabola: (y-75)^2 = 4*f*(x-100), f = 50, vertex (100,75), opening +X
f = 50.0
vx, vy = 100.0, 75.0
x_end = 200.0
t = 2.0  # small wall thickness to make the revolved reflector a solid shell

r_in_max = math.sqrt(4 * f * (x_end - vx))          # ~141.42
r_out_max = math.sqrt(4 * f * (x_end - (vx - t)))   # outer surface shifted -X by t

n = 40
inner = [(vx + (r_in_max * i / n) ** 2 / (4 * f), vy + r_in_max * i / n) for i in range(n + 1)]
outer = [((vx - t) + (r_out_max * i / n) ** 2 / (4 * f), vy + r_out_max * i / n) for i in range(n + 1)]
outer_rev = list(reversed(outer))

profile = (
    cq.Workplane("XY")
    .moveTo(*inner[0])
    .spline(inner[1:], includeCurrent=True)
    .lineTo(*outer_rev[0])
    .spline(outer_rev[1:], includeCurrent=True)
    .close()
)

# Revolve 360 deg about horizontal axis y = 75
result = profile.revolve(360, (0, vy, 0), (1, vy, 0))
