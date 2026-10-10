import cadquery as cq
import math

# --- parameters ---
R_out = 60.0
depth = 3.4
R_root = R_out - depth
W = 40.0
N = 47
pitch = 8.0
R_pitch = N * pitch / (2 * math.pi)
helix = math.radians(15)
twist_deg = math.degrees(W * math.tan(helix) / R_pitch)
R_rim_in = 52.0
R_hub = 22.5
R_bore = 12.5

# --- helical toothed rim body ---
p = 2 * math.pi / N
a = 2.3 / R_out  # groove half-width angle


def pt(r, t):
    return (r * math.cos(t), r * math.sin(t))


w = cq.Workplane("XY").workplane(offset=-W / 2).moveTo(*pt(R_out, -a))
for k in range(N):
    w = w.threePointArc(pt(R_root, k * p), pt(R_out, k * p + a))
    w = w.threePointArc(pt(R_out, (k + 0.5) * p), pt(R_out, (k + 1) * p - a))
w = w.close()
toothed = w.twistExtrude(W, twist_deg)

# chamfer 1.5x45 at rim edges via revolved envelope
c = 1.5
env = (
    cq.Workplane("XZ")
    .polyline([(0, -W / 2), (R_out - c, -W / 2), (R_out, -W / 2 + c),
               (R_out, W / 2 - c), (R_out - c, W / 2), (0, W / 2)])
    .close()
    .revolve(360, (0, 0, 0), (0, 1, 0))
)
rim = toothed.intersect(env)
rim = rim.cut(cq.Workplane("XY").circle(R_rim_in).extrude(W).translate((0, 0, -W / 2)))

# --- hub ---
hub = cq.Workplane("XY").circle(R_hub).extrude(W).translate((0, 0, -W / 2))

# --- twisted elliptical spoke ---
x0, x1 = 20.0, 54.0
n_sec = 9
dx = (x1 - x0) / (n_sec - 1)
sp = cq.Workplane("YZ").workplane(offset=x0)
for i in range(n_sec):
    t = i / (n_sec - 1)
    ang = 90.0 * (1 - t)  # 90 -> major axis along Z (axial); 0 -> along Y (circumferential)
    sp = sp.ellipse(6.0, 3.0, rotation_angle=ang)
    if i < n_sec - 1:
        sp = sp.workplane(offset=dx)
spoke = sp.loft(ruled=True, combine=True)

body = rim.union(hub)
for i in range(5):
    body = body.union(spoke.rotate((0, 0, 0), (0, 0, 1), i * 72))

# --- bore and keyway ---
bore = cq.Workplane("XY").circle(R_bore).extrude(W + 2).translate((0, 0, -W / 2 - 1))
key = cq.Workplane("XY").box(15.3, 6.0, W + 2, centered=(False, True, True))
body = body.cut(bore).cut(key)

result = body
