import cadquery as cq
import math

L, W, H = 150.0, 100.0, 30.0
dv_b, dv_h = 60.0, 15.0
ang = math.radians(60)
dv_t = dv_b + 2 * dv_h / math.tan(ang)  # dovetail wider at top

# Base block
base = cq.Workplane("XY").box(L, W, H, centered=(True, True, False))

# Dovetail rail along X
pts = [(-dv_b / 2, H), (dv_b / 2, H), (dv_t / 2, H + dv_h), (-dv_t / 2, H + dv_h)]
rail = (cq.Workplane("YZ", origin=(-L / 2, 0, 0))
        .polyline(pts).close().extrude(L))
body = base.union(rail)

# Side T-slots (on both 150x30 faces)
mouth_w, mouth_d = 10.0, 3.0
inner_w, inner_d = 16.0, 4.0
zc = H / 2
for s in (1, -1):
    mouth = (cq.Workplane("XY")
             .box(L + 2, mouth_d + 0.5, mouth_w)
             .translate((0, s * (W / 2 - mouth_d / 2 + 0.25), zc)))
    inner = (cq.Workplane("XY")
             .box(L + 2, inner_d, inner_w)
             .translate((0, s * (W / 2 - mouth_d - inner_d / 2), zc)))
    body = body.cut(mouth).cut(inner)

# Relief / oil grooves at rail root
for s in (1, -1):
    g = (cq.Workplane("XY").box(L + 2, 2.0, 1.0)
         .translate((0, s * (dv_b / 2), H - 0.5)))
    body = body.cut(g)

# Central counterbored hole
top = H + dv_h
thru = cq.Workplane("XY").circle(15.0).extrude(top + 2).translate((0, 0, -1))
cb = cq.Workplane("XY").circle(20.0).extrude(5.0 + 1).translate((0, 0, top - 5.0))
body = body.cut(thru).cut(cb)

# Four corner countersunk mounting holes
for x in (-65.0, 65.0):
    for y in (-40.0, 40.0):
        h = cq.Workplane("XY").circle(4.0).extrude(H + 2).translate((x, y, -1))
        cone = cq.Workplane("XY").add(
            cq.Solid.makeCone(4.0, 7.0, 3.0,
                              pnt=cq.Vector(x, y, H - 3.0),
                              dir=cq.Vector(0, 0, 1)))
        body = body.cut(h).cut(cone)

result = body
