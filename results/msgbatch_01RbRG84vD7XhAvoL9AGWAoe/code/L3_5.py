import cadquery as cq
import math

# Parameters
R_out = 100.0      # outer radius (OD 200)
t = 10.0           # wall thickness
H_flange = 50.0    # straight flange height
b_out = 50.0       # outer dome depth (2:1 ellipsoidal head, D/4)
R_in = R_out - t
b_in = b_out - t

noz_od = 40.0
noz_id = 30.0
noz_h = 30.0

def ellipsoid(a, b, zc):
    s = cq.Solid.makeSphere(a, angleDegrees1=-90, angleDegrees2=90)
    m = cq.Matrix([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, b / a, 0]])
    e = s.transformGeometry(m)
    return cq.Workplane("XY").add(e.translate(cq.Vector(0, 0, zc)))

# Outer solid
outer = (cq.Workplane("XY").circle(R_out).extrude(H_flange)
         .union(ellipsoid(R_out, b_out, H_flange)))
clip = cq.Workplane("XY").box(400, 400, 400, centered=(True, True, False))
outer = outer.intersect(clip)

# Inner void
inner = (cq.Workplane("XY").workplane(offset=-1).circle(R_in).extrude(H_flange + 1)
         .union(ellipsoid(R_in, b_in, H_flange)))

head = outer.cut(inner)

# Nozzle at apex
apex_z = H_flange + b_out
nozzle = (cq.Workplane("XY").workplane(offset=apex_z - t)
          .circle(noz_od / 2).extrude(noz_h + t))
head = head.union(nozzle)

# Bore through nozzle and dome
bore = (cq.Workplane("XY").workplane(offset=apex_z - 2 * t)
        .circle(noz_id / 2).extrude(noz_h + 3 * t))
head = head.cut(bore)

result = head
