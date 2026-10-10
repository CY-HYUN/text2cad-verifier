import cadquery as cq
import math

# ---------------- Parameters ----------------
N_TEETH = 47
PITCH = 8.0
R_OUT = 60.0                  # rim outer radius (OD 120)
FACE = 40.0                   # face width
TOOTH_DEPTH = 3.4
GROOVE_R = 2.6                # HTD-like arc groove radius
R_PITCH = N_TEETH * PITCH / (2 * math.pi)
HELIX = math.radians(15.0)
R_RIM_IN = 50.0               # rim inner radius
R_HUB = 22.5
R_BORE = 12.5
KEY_W = 6.0
KEY_TOP = R_BORE + 3.3
CHAMF = 1.5
N_SPOKES = 5

# ---------------- Helical toothed rim ----------------
c = R_OUT - TOOTH_DEPTH + GROOVE_R          # groove arc centre radius
cos_a = (c**2 + R_OUT**2 - GROOVE_R**2) / (2 * c * R_OUT)
alpha = math.acos(cos_a)                     # half angle of groove at OD
step = 2 * math.pi / N_TEETH

def pol(r, a):
    return (r * math.cos(a), r * math.sin(a))

wp = cq.Workplane("XY").moveTo(*pol(R_OUT, -alpha))
for i in range(N_TEETH):
    a0 = i * step
    # groove arc
    wp = wp.threePointArc(pol(c - GROOVE_R, a0), pol(R_OUT, a0 + alpha))
    # land arc
    wp = wp.threePointArc(pol(R_OUT, a0 + step / 2), pol(R_OUT, a0 + step - alpha))
wp = wp.close()

ext = 2.0
twist_deg = math.degrees((FACE + 2 * ext) * math.tan(HELIX) / R_PITCH)
teeth = (wp.twistExtrude(FACE + 2 * ext, twist_deg)
         .translate((0, 0, -ext)))

# chamfered rim envelope (revolved)
env_pts = [
    (R_RIM_IN + CHAMF, 0), (R_OUT - CHAMF, 0), (R_OUT, CHAMF),
    (R_OUT, FACE - CHAMF), (R_OUT - CHAMF, FACE), (R_RIM_IN + CHAMF, FACE),
    (R_RIM_IN, FACE - CHAMF), (R_RIM_IN, CHAMF),
]
envelope = (cq.Workplane("XZ").polyline(env_pts).close()
            .revolve(360, (0, 0, 0), (0, 1, 0)))
rim = teeth.intersect(envelope)

# ---------------- Hub ----------------
hub = cq.Workplane("XY").circle(R_HUB).extrude(FACE)

# ---------------- Twisted elliptical spokes ----------------
r_start, r_end = R_HUB - 2.0, R_RIM_IN + 2.0
n_st = 6
dl = (r_end - r_start) / (n_st - 1)
dang = 90.0 / (n_st - 1)
sp = cq.Workplane("YZ", origin=(0, 0, FACE / 2)).workplane(offset=r_start).ellipse(3.0, 6.0)
for k in range(1, n_st):
    sp = sp.workplane(offset=dl).transformed(rotate=(0, 0, dang)).ellipse(3.0, 6.0)
spoke = sp.loft(ruled=False)

body = rim.union(hub)
for i in range(N_SPOKES):
    body = body.union(spoke.rotate((0, 0, 0), (0, 0, 1), i * 360.0 / N_SPOKES))

# root fillets (best effort)
try:
    body = body.edges(
        cq.selectors.BoxSelector((-R_RIM_IN - 1, -R_RIM_IN - 1, 1), (R_RIM_IN + 1, R_RIM_IN + 1, FACE - 1))
    ).edges("not %CIRCLE").edges("not %LINE").fillet(4.0)
except Exception:
    pass

# ---------------- Bore and keyway ----------------
bore = cq.Workplane("XY").circle(R_BORE).extrude(FACE + 2).translate((0, 0, -1))
key = (cq.Workplane("XY").center((R_BORE + KEY_TOP) / 2 - 1, 0)
       .rect(KEY_TOP - R_BORE + 2, KEY_W).extrude(FACE + 2).translate((0, 0, -1)))
body = body.cut(bore).cut(key)

result = body
