import cadquery as cq
import math

# Parameters
r_mean = 20.0        # mean outer radius (40 mm mean diameter)
amp = 2.5            # 45/35 mm peak/trough diameters -> +/-2.5 mm
wall = 2.0
total = 100.0        # overall length including straight ends
end_len = 5.0
cycles = 10
wave_len = total - 2 * end_len      # 90 mm wavy section
wavelength = wave_len / cycles      # 9 mm per cycle

n = 20 * cycles  # sample points along the wave

def r_out(z):
    return r_mean + amp * math.sin(2 * math.pi * (z - end_len) / wavelength)

outer_pts = []
for i in range(1, n + 1):
    z = end_len + wave_len * i / n
    outer_pts.append((r_out(z), z))

inner_pts = []
for i in range(1, n + 1):
    z = end_len + wave_len - wave_len * i / n
    inner_pts.append((r_out(z) - wall, z))

profile = (
    cq.Workplane("XY")
    .moveTo(r_mean - wall, 0)
    .lineTo(r_mean, 0)
    .lineTo(r_mean, end_len)
    .spline(outer_pts, includeCurrent=True)
    .lineTo(r_mean, total)
    .lineTo(r_mean - wall, total)
    .lineTo(r_mean - wall, total - end_len)
    .spline(inner_pts, includeCurrent=True)
    .close()
)

bellows = profile.revolve(360, (0, 0, 0), (0, 1, 0))

# Orient the axis along Z
result = bellows.rotate((0, 0, 0), (1, 0, 0), 90)
