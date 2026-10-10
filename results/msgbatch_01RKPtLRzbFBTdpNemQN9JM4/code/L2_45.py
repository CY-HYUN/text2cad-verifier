import cadquery as cq
import math

L = 100.0
end_len = 5.0
wl = 10.0
amp = 2.5
r_mean = 20.0
t = 2.0
z0, z1 = end_len, L - end_len
n_cycles = (z1 - z0) / wl  # 9 cycles fit between the 5 mm straight ends
N = int(n_cycles * 20)

def r_out(z):
    return r_mean + amp * math.sin(2 * math.pi * (z - z0) / wl)

zs = [z0 + (z1 - z0) * i / N for i in range(N + 1)]
outer_pts = [(r_out(z), z) for z in zs[1:]]
inner_pts = [(r_out(z) - t, z) for z in reversed(zs)]
inner_pts = inner_pts[:-1] + [(r_mean - t, z0)]

prof = (
    cq.Workplane("XY")
    .moveTo(r_mean - t, 0)
    .lineTo(r_mean, 0)
    .lineTo(r_mean, z0)
    .spline(outer_pts, includeCurrent=True)
    .lineTo(r_mean, L)
    .lineTo(r_mean - t, L)
    .lineTo(r_mean - t, z1)
    .spline(inner_pts[1:], includeCurrent=True)
    .lineTo(r_mean - t, 0)
    .close()
)

result = prof.revolve(360, (0, 0, 0), (0, 1, 0))
