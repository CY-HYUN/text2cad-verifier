import cadquery as cq
import math

# ---------------- Parameters ----------------
N_TEETH = 47
PITCH = 8.0
R_OUT = 60.0
WIDTH = 40.0
TOOTH_DEPTH = 3.4
HELIX = math.radians(15.0)
R_PITCH = N_TEETH * PITCH / (2 * math.pi)
R_RIM_IN = 48.0
CH = 1.5

HUB_R = 22.5
BORE_R = 12.5
KEY_W = 6.0
KEY_D = 3.3

N_SPOKES = 5
ELL_A = 6.0   # semi-major
ELL_B = 3.0   # semi-minor
FILLET_R = 4.0

# ---------------- Toothed rim (helical) ----------------
groove_half = 2.8  # half width of HTD groove at the OD (mm of arc)
pts = []
samples_per_tooth = 18
ang_pitch = 2 * math.pi / N_TEETH
for i in range(N_TEETH * samples_per_tooth):
    th = i * ang_pitch / samples_per_tooth
    local = (th % ang_pitch) - ang_pitch / 2.0
    s = local * R_OUT
    if abs(s) < groove_half:
        d = TOOTH_DEPTH * math.sqrt(max(0.0, 1 - (s / groove_half) ** 2))
    else:
        d = 0.0
    r = R_OUT - d
    pts.append((r * math.cos(th), r * math.sin(th)))

twist_deg = math.degrees(WIDTH * math.tan(HELIX) / R_PITCH)

toothed = (
    cq.Workplane("XY")
    .workplane(offset=-WIDTH / 2)
    .spline(pts, periodic=True)
    .close()
    .twistExtrude(WIDTH, twist_deg)
)

# Chamfered annulus envelope (gives 1.5x45 chamfers on rim edges)
z0, z1 = -WIDTH / 2, WIDTH / 2
prof = [
    (R_RIM_IN, z0 + CH), (R_RIM_IN + CH, z0), (R_OUT - CH, z0), (R_OUT, z0 + CH),
    (R_OUT, z1 - CH), (R_OUT - CH, z1), (R_RIM_IN + CH, z1), (R_RIM_IN, z1 - CH),
]
envelope = cq.Workplane("XZ").polyline(prof).close().revolve(360, (0, 0, 0), (0, 1, 0))

rim = toothed.intersect(envelope)

# ---------------- Hub ----------------
hub = (
    cq.Workplane("XY")
    .workplane(offset=-WIDTH / 2)
    .circle(HUB_R)
    .extrude(WIDTH)
)

# ---------------- Twisted elliptical spokes ----------------
r_start = HUB_R - 3.0
r_end = R_RIM_IN + 3.0
n_sec = 6
wp = cq.Workplane("YZ").workplane(offset=r_start)
step = (r_end - r_start) / (n_sec - 1)
for k in range(n_sec):
    t = k / (n_sec - 1)
    if k > 0:
        wp = wp.workplane(offset=step)
    # major axis along Z (axial) at hub -> along Y (circumferential) at rim
    wp = wp.ellipse(ELL_A, ELL_B, rotation_angle=90.0 * (1 - t))
spoke = wp.loft(ruled=False, combine=True)

body = rim.union(hub)
for i in range(N_SPOKES):
    body = body.union(spoke.rotate((0, 0, 0), (0, 0, 1), i * 360.0 / N_SPOKES))

# ---------------- Root fillets (best effort) ----------------
try:
    def root_edge(e):
        c = e.Center()
        rr = math.hypot(c.x, c.y)
        return (abs(rr - HUB_R) < 3.5 or abs(rr - R_RIM_IN) < 3.5) and e.geomType() not in ("LINE", "CIRCLE")
    edges = [e for e in body.val().Edges() if root_edge(e)]
    if edges:
        filleted = body.val().fillet(FILLET_R, edges)
        if filleted.isValid():
            body = cq.Workplane("XY").newObject([filleted])
except Exception:
    pass

# ---------------- Bore and keyway ----------------
bore = (
    cq.Workplane("XY")
    .workplane(offset=-WIDTH / 2 - 1)
    .circle(BORE_R)
    .extrude(WIDTH + 2)
)
key = (
    cq.Workplane("XY")
    .box(KEY_D + 2.0, KEY_W, WIDTH + 2)
    .translate((BORE_R + KEY_D / 2 - 1.0, 0, 0))
)
body = body.cut(bore).cut(key)

result = body
