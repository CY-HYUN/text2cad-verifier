import cadquery as cq
import math

# ---------------- Base block ----------------
cube_size = 60.0
body = cq.Workplane("XY").box(cube_size, cube_size, cube_size).edges().fillet(10.0)

# ---------------- Top / bottom pipes with square flanges ----------------
for s in (1, -1):
    pipe = (cq.Workplane("XY").circle(20.0).extrude(30.0)
            .translate((0, 0, 30.0)) if s == 1 else
            cq.Workplane("XY").circle(20.0).extrude(30.0).translate((0, 0, -60.0)))
    body = body.union(pipe)
    zc = s * 56.0
    flange = cq.Workplane("XY").box(60.0, 60.0, 8.0).translate((0, 0, zc))
    body = body.union(flange)

# ---------------- Side pipes with circular flanges ----------------
side_dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
for dx, dy in side_dirs:
    ang = math.degrees(math.atan2(dy, dx))
    pipe = (cq.Workplane("YZ").circle(15.0).extrude(25.0)
            .translate((30.0, 0, 0)))
    flange = (cq.Workplane("YZ").circle(25.0).extrude(6.0)
              .translate((49.0, 0, 0)))
    part = pipe.union(flange).rotate((0, 0, 0), (0, 0, 1), ang)
    body = body.union(part)

# ---------------- Reinforcement ribs ----------------
rib_pts = [(18.0, 30.0), (38.0, 30.0), (18.0, 50.0)]
for zs in (1, -1):
    pts = [(x, z * zs) for x, z in rib_pts]
    for a in (45, 135, 225, 315):
        rib = (cq.Workplane("XZ").polyline(pts).close()
               .extrude(2.5, both=True)
               .rotate((0, 0, 0), (0, 0, 1), a))
        body = body.union(rib)

# ---------------- Central spherical cavity ----------------
body = body.cut(cq.Workplane("XY").sphere(20.0))

# ---------------- Flow channel bores ----------------
vbore = cq.Workplane("XY").circle(14.0).extrude(140.0).translate((0, 0, -70.0))
body = body.cut(vbore)
for dx, dy in side_dirs:
    ang = math.degrees(math.atan2(dy, dx))
    hb = (cq.Workplane("YZ").circle(10.0).extrude(65.0)
          .rotate((0, 0, 0), (0, 0, 1), ang))
    body = body.cut(hb)

# ---------------- Bolt holes: square flanges ----------------
for zs in (1, -1):
    for px in (-22.0, 22.0):
        for py in (-22.0, 22.0):
            h = (cq.Workplane("XY").circle(3.25).extrude(20.0)
                 .translate((px, py, 50.0 if zs == 1 else -70.0)))
            body = body.cut(h)

# ---------------- Bolt holes: circular flanges ----------------
pcd_r = 20.0
for dx, dy in side_dirs:
    ang = math.degrees(math.atan2(dy, dx))
    for k in range(4):
        t = math.radians(45 + 90 * k)
        h = (cq.Workplane("YZ").circle(2.75).extrude(15.0)
             .translate((45.0, pcd_r * math.cos(t), pcd_r * math.sin(t)))
             .rotate((0, 0, 0), (0, 0, 1), ang))
        body = body.cut(h)

result = body
