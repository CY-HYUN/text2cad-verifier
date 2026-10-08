import cadquery as cq
import math

# Inner contour parameters
r_t = 5.0          # throat radius
z_t = 20.0         # throat axial position
R_arc = 50.0       # inlet arc radius
r_exit = 20.0      # exit radius
L = 100.0

def r_conv(z):
    return (r_t + R_arc) - math.sqrt(R_arc**2 - (z - z_t)**2)

k = (r_exit - r_t) / (L - z_t) ** 2
def r_div(z):
    return r_t + k * (z - z_t) ** 2

# Outer ellipse (center z=50, semi-axes a=80 axial, b=30 radial)
a_e, b_e, zc = 80.0, 30.0, 50.0
def r_out(z):
    return b_e * math.sqrt(1 - ((z - zc) / a_e) ** 2)

r_in0 = r_conv(0.0)
fl_t = 5.0
fl_r = 30.0

n = 20
ell_pts = [(r_out(5 + 90 * i / n), 5 + 90 * i / n) for i in range(n + 1)]
par_pts = [(r_div(L - (L - z_t) * i / n), L - (L - z_t) * i / n) for i in range(n + 1)]

prof = (
    cq.Workplane("XZ")
    .moveTo(r_in0, 0)
    .lineTo(fl_r, 0)
    .lineTo(fl_r, fl_t)
    .lineTo(ell_pts[0][0], ell_pts[0][1])
    .spline(ell_pts[1:], includeCurrent=True)
    .lineTo(fl_r, L - fl_t)
    .lineTo(fl_r, L)
    .lineTo(r_exit, L)
    .spline(par_pts[1:], includeCurrent=True)
    .threePointArc((r_conv(10.0), 10.0), (r_in0, 0))
    .close()
)

result = prof.revolve(360, (0, 0, 0), (0, 1, 0))
