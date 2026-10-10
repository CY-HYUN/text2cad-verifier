import cadquery as cq
import math

# Inner contour
R_arc = 50.0
r_throat = 5.0
z_throat = 20.0
L = 100.0
r_exit = 20.0

def r_in(z):
    if z <= z_throat:
        return (r_throat + R_arc) - math.sqrt(R_arc**2 - (z - z_throat)**2)
    t = (z - z_throat) / (L - z_throat)
    return r_throat + (r_exit - r_throat) * t * t  # parabola, vertex at throat

# Outer elliptical contour, max radius 30 at mid-length
R_max = 30.0
zc = 50.0
a = 50.0 / math.sqrt(1 - (25.0 / 30.0) ** 2)  # r_out=25 at ends

def r_out(z):
    return R_max * math.sqrt(1 - ((z - zc) / a) ** 2)

fl_t = 5.0
fl_r = 30.0

pts = []
# inlet face
pts.append((r_in(0), 0))
pts.append((fl_r, 0))
pts.append((fl_r, fl_t))
# outer ellipse
n = 40
for i in range(n + 1):
    z = fl_t + (L - 2 * fl_t) * i / n
    pts.append((r_out(z), z))
# outlet flange
pts.append((fl_r, L - fl_t))
pts.append((fl_r, L))
# inner contour back from exit to inlet
m = 80
inner = []
for i in range(m + 1):
    z = L - L * i / m
    inner.append((r_in(z), z))
pts.extend(inner)

# remove consecutive duplicates
clean = []
for p in pts:
    if not clean or (abs(clean[-1][0] - p[0]) > 1e-6 or abs(clean[-1][1] - p[1]) > 1e-6):
        clean.append(p)
if abs(clean[-1][0] - clean[0][0]) < 1e-6 and abs(clean[-1][1] - clean[0][1]) < 1e-6:
    clean.pop()

result = (
    cq.Workplane("XY")
    .polyline(clean)
    .close()
    .revolve(360, (0, 0, 0), (0, 1, 0))
)
