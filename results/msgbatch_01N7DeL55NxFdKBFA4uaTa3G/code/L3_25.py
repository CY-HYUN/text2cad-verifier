import cadquery as cq
import math

# Parameters
R_out = 60.0        # sleeve outer radius (OD 120)
R_in = 40.0         # sleeve bore radius (ID 80)
H = 100.0           # sleeve height
fin_R = 80.0        # fin outer radius (OD 160)
fin_t = 2.0
n_fins = 15
fin_z0 = 2.0
fin_pitch = (H - 2 * fin_z0 - fin_t) / (n_fins - 1)

# Hollow cylinder sleeve
sleeve = (cq.Workplane("XY").circle(R_out).circle(R_in).extrude(H))

# Cooling fins (linear array along Z)
body = sleeve
for i in range(n_fins):
    z = fin_z0 + i * fin_pitch
    fin = (cq.Workplane("XY").workplane(offset=z)
           .circle(fin_R).circle(R_out - 0.5).extrude(fin_t))
    body = body.union(fin)

# Hemispherical combustion chamber cover
center = cq.Vector(0, 0, H)
dome = cq.Workplane("XY").add(
    cq.Solid.makeSphere(R_out, pnt=center, angleDegrees1=0, angleDegrees2=90))
body = body.union(dome)

# Combustion chamber cavity (inner hemisphere)
cavity = cq.Workplane("XY").add(
    cq.Solid.makeSphere(R_in, pnt=center, angleDegrees1=0, angleDegrees2=90))
body = body.cut(cavity)

# Intake / exhaust tubes on asymmetric inclined axes
def tube(az_deg, el_deg, y_off, ro=15.0, ri=10.0):
    az, el = math.radians(az_deg), math.radians(el_deg)
    d = cq.Vector(math.cos(el) * math.cos(az), math.cos(el) * math.sin(az), math.sin(el))
    base = center + cq.Vector(0, y_off, 0)
    outer = cq.Solid.makeCylinder(ro, 45.0, base + d * 45.0, d)
    inner = cq.Solid.makeCylinder(ri, 75.0, base + d * 20.0, d)
    return outer, inner

t1o, t1i = tube(0, 45, 12.0)      # intake
t2o, t2i = tube(180, 30, -12.0)   # exhaust
body = body.union(cq.Workplane("XY").add(t1o)).union(cq.Workplane("XY").add(t2o))
body = body.cut(cq.Workplane("XY").add(t1i)).cut(cq.Workplane("XY").add(t2i))

# Spark plug hole from apex vertically downward
plug = (cq.Workplane("XY").workplane(offset=H - 5)
        .circle(7.0).extrude(R_out + 20))
body = body.cut(plug)

# Four bolt column holes at quadrant points, through full height
bolt_r = (R_out + R_in) / 2.0
bolts = (cq.Workplane("XY").workplane(offset=-5)
         .pushPoints([(bolt_r, 0), (0, bolt_r), (-bolt_r, 0), (0, -bolt_r)])
         .circle(4.0).extrude(H + R_out + 20))
body = body.cut(bolts)

result = body
