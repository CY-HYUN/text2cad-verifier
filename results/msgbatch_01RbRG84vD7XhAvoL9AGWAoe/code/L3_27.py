import cadquery as cq
import math

# --- Core block: 60 mm cube with corners rounded by intersecting with a sphere ---
cube = cq.Workplane("XY").box(60, 60, 60)
sph = cq.Workplane("XY").sphere(48)
body = cube.intersect(sph)

# --- Top / bottom pipes (OD 40, length 30) with square flanges 60x60 ---
for sgn in (1, -1):
    pipe = (cq.Workplane("XY").circle(20).extrude(30)
            .translate((0, 0, 30)) if sgn > 0 else
            cq.Workplane("XY").circle(20).extrude(30).translate((0, 0, -60)))
    body = body.union(pipe)
    fl_z = 56 if sgn > 0 else -56
    flange = cq.Workplane("XY").box(60, 60, 8).translate((0, 0, fl_z))
    holes = (cq.Workplane("XY")
             .pushPoints([(22, 22), (-22, 22), (22, -22), (-22, -22)])
             .circle(3).extrude(10).translate((0, 0, fl_z - 5)))
    flange = flange.cut(holes)
    body = body.union(flange)

# --- Side pipes (OD 30, length 25) with circular flanges D50 ---
def side_port():
    p = cq.Workplane("YZ").circle(15).extrude(25).translate((30, 0, 0))
    fl = cq.Workplane("YZ").circle(25).extrude(6).translate((49, 0, 0))
    pts = [(20 * math.cos(math.radians(a)), 20 * math.sin(math.radians(a)))
           for a in (45, 135, 225, 315)]
    h = cq.Workplane("YZ").pushPoints(pts).circle(2.5).extrude(10).translate((47, 0, 0))
    return p.union(fl.cut(h))

for ang in (0, 90, 180, 270):
    body = body.union(side_port().rotate((0, 0, 0), (0, 0, 1), ang))

# --- Triangular reinforcing ribs at top and bottom pipe junctions ---
rib = (cq.Workplane("XZ")
       .polyline([(15, 29), (34, 29), (15, 52)]).close()
       .extrude(2.5, both=True))
for ang in (45, 135, 225, 315):
    r = rib.rotate((0, 0, 0), (0, 0, 1), ang)
    body = body.union(r)
    body = body.union(r.mirror("XY"))

# --- Internal cavity and flow channels ---
cavity = cq.Workplane("XY").sphere(20)
vbore = cq.Workplane("XY").circle(14).extrude(130).translate((0, 0, -65))
xbore = cq.Workplane("YZ").circle(10).extrude(120).translate((-60, 0, 0))
ybore = cq.Workplane("XZ").circle(10).extrude(120).translate((0, 60, 0))
body = body.cut(cavity).cut(vbore).cut(xbore).cut(ybore)

result = body
