import cadquery as cq
import math

# ---------------- Parameters ----------------
N_TEETH = 47
PITCH = 8.0
R_OUT = 60.0              # outer radius of the rim (D = 120)
WIDTH = 40.0              # face width
TOOTH_DEPTH = 3.4
BETA = math.radians(15.0)
R_PITCH = N_TEETH * PITCH / (2 * math.pi)
R_RIM_IN = 50.0           # inner wall of the rim
CHAMFER = 1.5

HUB_R = 22.5
BORE_R = 12.5
KEY_W = 6.0
KEY_DEPTH = 3.3

ELL_MAJ = 6.0             # semi-major (12 mm major axis)
ELL_MIN = 3.0             # semi-minor (6 mm minor axis)
N_SPOKES = 5
FILLET_R = 4.0

# ---------------- Toothed profile (HTD-like arc grooves) ----------------
g_r = 2.6
g_c = R_OUT - TOOTH_DEPTH + g_r          # groove circle centre radius
cos_a0 = (R_OUT**2 - g_c**2 - g_r**2) / (2 * g_c * g_r)
a0 = math.acos(cos_a0)
# angular half-width of groove at the outer circle
p_int = (g_c + g_r * math.cos(a0), g_r * math.sin(a0))
half_ang = math.atan2(p_int[1], p_int[0])

pts = []
step = 2 * math.pi / N_TEETH
n_g = 12
n_o = 4
for i in range(N_TEETH):
    phi = i * step
    c, s = math.cos(phi), math.sin(phi)
    # groove arc (local frame: x radial, y tangential), from +a0 through pi to -a0
    for k in range(n_g + 1):
        a = a0 + (2 * math.pi - 2 * a0) * k / n_g
        lx = g_c + g_r * math.cos(a)
        ly = -g_r * math.sin(a)  # go clockwise -> increasing global angle ordering
        pts.append((lx * c - ly * s, lx * s + ly * c))
    # outer land arc to next groove
    t0 = phi + half_ang
    t1 = phi + step - half_ang
    for k in range(1, n_o):
        t = t0 + (t1 - t0) * k / n_o
        pts.append((R_OUT * math.cos(t), R_OUT * math.sin(t)))

# check orientation ordering (ensure increasing angle); reverse groove ordering if needed
def ang(p):
    return math.atan2(p[1], p[0])
if ang(pts[0]) > ang(pts[n_g]):
    pass  # ordering already consistent in global sense

twist_deg = math.degrees(WIDTH * math.tan(BETA) / R_PITCH)

toothed = (
    cq.Workplane("XY")
    .workplane(offset=-WIDTH / 2)
    .polyline(pts).close()
    .twistExtrude(WIDTH, twist_deg)
)

# Ring envelope with 1.5x45 chamfers on all four rim edges
h = WIDTH / 2
ring_prof = [
    (R_RIM_IN + CHAMFER, -h), (R_OUT - CHAMFER, -h), (R_OUT, -h + CHAMFER),
    (R_OUT, h - CHAMFER), (R_OUT - CHAMFER, h), (R_RIM_IN + CHAMFER, h),
    (R_RIM_IN, h - CHAMFER), (R_RIM_IN, -h + CHAMFER),
]
ring = (
    cq.Workplane("XZ").polyline(ring_prof).close()
    .revolve(360, (0, 0, 0), (0, 1, 0))
)
rim = toothed.intersect(ring)

# ---------------- Hub ----------------
hub = cq.Workplane("XY").circle(HUB_R).extrude(WIDTH / 2, both=True)

# ---------------- Twisted elliptical spokes ----------------
x_start = HUB_R - 3.0
x_end = R_RIM_IN + 3.0
n_sec = 5
dx = (x_end - x_start) / (n_sec - 1)
wp = cq.Workplane("YZ").workplane(offset=x_start)
for k in range(n_sec):
    rot = 90.0 * k / (n_sec - 1)
    if k > 0:
        wp = wp.workplane(offset=dx)
    wp = wp.ellipse(ELL_MIN, ELL_MAJ, rotation_angle=rot)
spoke = wp.loft(ruled=False)

body = rim.union(hub)
for i in range(N_SPOKES):
    body = body.union(spoke.rotate((0, 0, 0), (0, 0, 1), i * 360.0 / N_SPOKES))

# ---------------- Root fillets (best effort) ----------------
try:
    def near_root(e):
        c = e.Center()
        r = math.hypot(c.x, c.y)
        return (abs(r - HUB_R) < 3.5 or abs(r - R_RIM_IN) < 3.5) and abs(c.z) < h - 0.5
    edges = [e for e in body.edges().vals() if near_root(e)]
    if edges:
        filleted = body.newObject(edges).fillet(FILLET_R)
        if filleted.val().isValid():
            body = filleted
except Exception:
    pass

# ---------------- B