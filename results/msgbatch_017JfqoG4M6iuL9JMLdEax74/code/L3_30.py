import cadquery as cq
import math

L, W, H = 150.0, 100.0, 30.0
rail_bw, rail_h, ang = 60.0, 15.0, 60.0
off = rail_h / math.tan(math.radians(ang))
rail_tw = rail_bw + 2 * off

# Base block
base = cq.Workplane("XY").box(L, W, H, centered=(True, True, False))

# Dovetail rail (wider at top), profile in YZ plane, extruded along X
rail = (cq.Workplane("YZ")
        .polyline([(-rail_bw / 2, H), (rail_bw / 2, H),
                   (rail_tw / 2, H + rail_h), (-rail_tw / 2, H + rail_h)])
        .close()
        .extrude(L / 2, both=True))
body = base.union(rail)

# Side T-slots on 150x30 faces, running full length
zc = H / 2
mouth_w, inner_w = 10.0, 16.0
mouth_d, inner_d = 4.0, 5.0
for s in (1, -1):
    y_face = s * W / 2
    mouth = (cq.Workplane("XY")
             .box(L + 2, mouth_d, mouth_w)
             .translate((0, y_face - s * mouth_d / 2, zc)))
    inner = (cq.Workplane("XY")
             .box(L + 2, inner_d, inner_w)
             .translate((0, y_face - s * (mouth_d + inner_d / 2), zc)))
    body = body.cut(mouth).cut(inner)

# Oil / tool relief grooves at root of rail (2 wide, 1 deep)
for s in (1, -1):
    g = (cq.Workplane("XY")
         .box(L + 2, 2.0, 1.0)
         .translate((0, s * (rail_bw / 2 + 1.0), H - 0.5)))
    body = body.cut(g)

# Central counterbored hole from rail top
body = (body.faces(">Z").workplane(centerOption="CenterOfBoundBox")
        .cboreHole(30.0, 40.0, 5.0))

# Four corner countersunk mounting holes from base top surface
pts = [(sx * 63.0, sy * 42.0) for sx in (1, -1) for sy in (1, -1)]
body = (body.faces(">Z").workplane(origin=(0, 0, H))
        .pushPoints(pts)
        .cskHole(8.0, 16.0, 90.0))

result = body
