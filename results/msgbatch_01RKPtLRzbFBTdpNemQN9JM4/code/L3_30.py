import cadquery as cq
import math

L, W, H = 150.0, 100.0, 30.0

# base block (x: length, y: width, z: height), z from 0 to 30
base = cq.Workplane("XY").box(L, W, H, centered=(True, True, False))

# dovetail rail: bottom width 60, height 15, side angle 60 deg (wider at top)
rh = 15.0
bw = 60.0
tw = bw + 2 * rh / math.tan(math.radians(60))
rail = (cq.Workplane("YZ").workplane(offset=-L / 2)
        .polyline([(-bw / 2, H), (bw / 2, H), (tw / 2, H + rh), (-tw / 2, H + rh)]).close()
        .extrude(L))
body = base.union(rail)

# oil / relief grooves at rail root (2 wide, 1 deep)
for s in (-1, 1):
    g = cq.Workplane("XY").box(L, 2.0, 1.0, centered=(True, True, False)).translate((0, s * (bw / 2 + 1.0), H - 1.0))
    body = body.cut(g)

# T-slots on both side faces, full length
zc = 12.0
neck, depth = 3.0, 8.0
for s in (-1, 1):
    pts = [(0, -5), (neck, -5), (neck, -8), (depth, -8), (depth, 8), (neck, 8), (neck, 5), (0, 5)]
    pts = [(s * (W / 2 - d), zc + z) for d, z in [(p[0], p[1]) for p in pts]]
    slot = (cq.Workplane("YZ").workplane(offset=-L / 2)
            .polyline(pts).close().extrude(L))
    body = body.cut(slot)

# central countersunk hole: 30 through, 40 x 5 counterbore from rail top
top = H + rh
body = body.cut(cq.Workplane("XY").circle(15).extrude(top))
body = body.cut(cq.Workplane("XY").workplane(offset=top - 5).circle(20).extrude(5))

# four corner countersunk mounting holes: dia 8, counterbore dia 14 x 4
for sx in (-1, 1):
    for sy in (-1, 1):
        x, y = sx * 64.0, sy * 44.0
        body = body.cut(cq.Workplane("XY").center(x, y).circle(4).extrude(H))
        body = body.cut(cq.Workplane("XY").workplane(offset=H - 4).center(x, y).circle(7).extrude(4))

result = body
