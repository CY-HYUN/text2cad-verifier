import cadquery as cq
import math

# ---------------- Parameters ----------------
cube = 60.0
fillet_r = 10.0
cavity_d = 40.0

vp_od, vp_len, vp_bore = 40.0, 30.0, 28.0      # vertical pipes
sq_fl, sq_t = 60.0, 8.0                         # square flange
sq_bolt_off, sq_bolt_d = 22.0, 6.6

hp_od, hp_len, hp_bore = 30.0, 25.0, 20.0      # horizontal pipes
c_fl_d, c_fl_t = 50.0, 6.0                      # circular flange
c_bolt_r, c_bolt_d = 20.0, 5.5

h = cube / 2.0

# ---------------- Base block ----------------
body = cq.Workplane("XY").box(cube, cube, cube).edges().fillet(fillet_r)

# ---------------- Vertical pipes + square flanges ----------------
for s in (1, -1):
    pipe = cq.Solid.makeCylinder(vp_od / 2, vp_len + 1,
                                 cq.Vector(0, 0, s * (h - 1)), cq.Vector(0, 0, s))
    body = body.union(cq.Workplane().add(pipe))
    zc = s * (h + vp_len - sq_t / 2)
    fl = cq.Workplane("XY").box(sq_fl, sq_fl, sq_t).translate((0, 0, zc))
    body = body.union(fl)

# ---------------- Horizontal pipes + circular flanges ----------------
dirs = [cq.Vector(1, 0, 0), cq.Vector(-1, 0, 0), cq.Vector(0, 1, 0), cq.Vector(0, -1, 0)]
for d in dirs:
    pipe = cq.Solid.makeCylinder(hp_od / 2, hp_len + 1, d * (h - 1), d)
    body = body.union(cq.Workplane().add(pipe))
    fl = cq.Solid.makeCylinder(c_fl_d / 2, c_fl_t, d * (h + hp_len - c_fl_t), d)
    body = body.union(cq.Workplane().add(fl))

# ---------------- Gussets (triangular plates) ----------------
for s in (1, -1):
    pts = [(vp_od / 2 - 2, s * (h - 0.5)), (36.0, s * (h - 0.5)), (vp_od / 2 - 2, s * 50.0)]
    g = cq.Workplane("XZ").polyline(pts).close().extrude(2.0, both=True)
    for k in range(4):
        body = body.union(g.rotate((0, 0, 0), (0, 0, 1), 45 + 90 * k))

# ---------------- Central cavity ----------------
body = body.cut(cq.Workplane().sphere(cavity_d / 2))

# ---------------- Flow bores ----------------
total_v = h + vp_len
vb = cq.Solid.makeCylinder(vp_bore / 2, 2 * total_v + 2,
                           cq.Vector(0, 0, -total_v - 1), cq.Vector(0, 0, 1))
body = body.cut(cq.Workplane().add(vb))
for d in dirs:
    hb = cq.Solid.makeCylinder(hp_bore / 2, h + hp_len + 1, cq.Vector(0, 0, 0), d)
    body = body.cut(cq.Workplane().add(hb))

# ---------------- Bolt holes: square flanges ----------------
for s in (1, -1):
    z0 = s * (total_v + 1)
    for x in (sq_bolt_off, -sq_bolt_off):
        for y in (sq_bolt_off, -sq_bolt_off):
            hole = cq.Solid.makeCylinder(sq_bolt_d / 2, sq_t + 2,
                                         cq.Vector(x, y, z0), cq.Vector(0, 0, -s))
            body = body.cut(cq.Workplane().add(hole))

# ---------------- Bolt holes: circular flanges ----------------
total_h = h + hp_len
for d in dirs:
    # two perpendicular axes in flange plane
    if abs(d.x) > 0:
        u, v = cq.Vector(0, 1, 0), cq.Vector(0, 0, 1)
    else:
        u, v = cq.Vector(1, 0, 0), cq.Vector(0, 0, 1)
    for k in range(4):
        a = math.radians(45 + 90 * k)
        off = u * (c_bolt_r * math.cos(a)) + v * (c_bolt_r * math.sin(a))
        start = d * (total_h + 1) + off
        hole = cq.Solid.makeCylinder(c_bolt_d / 2, c_fl_t + 2, start, d * -1)
        body = body.cut(cq.Workplane().add(hole))

result = body
