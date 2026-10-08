import cadquery as cq
import math

# Parameters
H = 80.0          # cup height
R_top = 80.0      # top inner radius
t = 5.0           # shell thickness
fl_w = 10.0       # flange width beyond outer shell
fl_t = 5.0        # flange thickness
fl_R = 95.0       # flange outer radius
hole_d = 5.0
hole_r = 90.0
light_d = 10.0

def z_in(r):
    return r * r / 80.0

N = 40
inner_pts = [(R_top * i / N, z_in(R_top * i / N)) for i in range(N + 1)]

# Outward normal offset of the parabola
outer_pts = []
for i in range(N + 1):
    r = R_top * i / N
    s = r / 40.0  # dz/dr
    n = math.sqrt(1 + s * s)
    outer_pts.append((r + t * s / n, z_in(r) - t / n))

outer_rev = list(reversed(outer_pts))
end_outer = outer_rev[0]

prof = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .spline(inner_pts[1:], includeCurrent=True)
    .lineTo(R_top + t, H)
    .lineTo(end_outer[0], end_outer[1])
    .spline(outer_rev[1:], includeCurrent=True)
    .close()
)
shell = prof.revolve(360, (0, 0, 0), (0, 1, 0))

# Flange: bottom flush with cup opening (z = H)
flange = (
    cq.Workplane("XY")
    .workplane(offset=H)
    .circle(fl_R)
    .circle(R_top)
    .extrude(fl_t)
)
body = shell.union(flange)

# Mounting holes (one on +Y)
holes = (
    cq.Workplane("XY")
    .workplane(offset=H - 1)
    .pushPoints([(0, hole_r), (hole_r, 0), (0, -hole_r), (-hole_r, 0)])
    .circle(hole_d / 2)
    .extrude(fl_t + 2)
)
body = body.cut(holes)

# Light source hole at bottom center
light = (
    cq.Workplane("XY")
    .workplane(offset=-t - 5)
    .circle(light_d / 2)
    .extrude(t + 15)
)
body = body.cut(light)

result = body
