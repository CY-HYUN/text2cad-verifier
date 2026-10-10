import cadquery as cq
import math

# --- parameters ---
R_out = 60.0
W = 40.0
N = 47
depth = 3.4
R_root = R_out - depth
R_pitch = N * 8.0 / (2 * math.pi)
helix = math.radians(15)
twist_deg = math.degrees(W * math.tan(helix) / R_pitch)
R_rim_in = 52.0
R_hub = 22.5
R_bore = 12.5

# --- toothed profile (arc grooves) ---
pitch_ang = 2 * math.pi / N
half_groove = 2.6 / R_out  # angular half-width of groove at tip

def P(r, a):
    return (r * math.cos(a), r * math.sin(a))

wp = cq.Workplane("XY").moveTo(*P(R_out, -half_groove))
for i in range(N):
    a = i * pitch_ang
    # groove centered at angle a
    wp = wp.threePointArc(P(R_root, a), P(R_out, a + half_groove))
    # land to next groove
    na = (i + 1) * pitch_ang
    mid = (a + half_groove + na - half_groove) / 2
    wp = wp.threePointArc(P(R_out, mid), P(R_out, na - half_groove))
wp = wp.close()
toothed = wp.twistExtrude(W, twist_deg)

# chamfered envelope (1.5 x 45 deg on rim edges)
env = cq.Workplane("XY").circle(R_out).extrude(W).faces(">Z or <Z").chamfer(1.5)
rim = toothed.intersect(env)
rim = rim.cut(cq.Workplane("XY").circle(R_rim_in).extrude(W))

# --- hub ---
hub = cq.Workplane("XY").circle(R_hub).extrude(W)

# --- twisted elliptical spokes ---
x0, x1 = 20.0, 54.0
nsec = 7
wires = []
for k in range(nsec):
    t = k / (nsec - 1)
    x = x0 + (x1 - x0) * t
    ang = 90.0 * t
    w = (cq.Workplane("YZ").workplane(offset=x)
         .transformed(rotate=(0, 0, ang))
         .ellipse(3.0, 6.0).val())
    wires.append(w)
spoke_solid = cq.Solid.makeLoft(wires, False)
spoke_solid = spoke_solid.translate(cq.Vector(0, 0, W / 2))

body = rim.union(hub)
for k in range(5):
    s = spoke_solid.rotate(cq.Vector(0, 0, 0), cq.Vector(0, 0, 1), k * 72.0)
    body = body.union(cq.Workplane("XY").add(s))

# --- bore and keyway ---
body = body.cut(cq.Workplane("XY").circle(R_bore).extrude(W))
key = cq.Workplane("XY").box(6.0, 5.0, W, centered=(True, False, False)).translate((0, 10.0, 0))
body = body.cut(key)

result = body
