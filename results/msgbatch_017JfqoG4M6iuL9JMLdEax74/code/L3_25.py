import cadquery as cq
import math

# Main dimensions
R_liner = 60.0
H = 100.0
R_bore = 40.0
R_fin = 80.0
fin_t = 2.0
n_fins = 15

# Cylinder liner
body = cq.Workplane("XY").circle(R_liner).extrude(H)

# Cooling fins
pitch = H / n_fins
for i in range(n_fins):
    z0 = i * pitch + (pitch - fin_t) / 2.0
    fin = (cq.Workplane("XY").workplane(offset=z0)
           .circle(R_fin).circle(R_liner - 1).extrude(fin_t))
    body = body.union(fin)

# Hemispherical combustion chamber cover
dome = cq.Workplane("XY").add(
    cq.Solid.makeSphere(R_liner, cq.Vector(0, 0, H), angleDegrees1=0, angleDegrees2=90))
body = body.union(dome)

# Intake / exhaust ports (asymmetric oblique pipes)
center = cq.Vector(0, 0, H)
pipes = [
    # (angle from vertical deg, azimuth deg, outer r, inner r, length)
    (40.0, 0.0, 15.0, 10.0, 95.0),    # intake
    (55.0, 180.0, 13.0, 8.5, 90.0),   # exhaust
]
bores = []
for ang, az, ro, ri, L in pipes:
    a = math.radians(ang)
    b = math.radians(az)
    d = cq.Vector(math.sin(a) * math.cos(b), math.sin(a) * math.sin(b), math.cos(a))
    p = cq.Solid.makeCylinder(ro, L, center, d)
    body = body.union(cq.Workplane("XY").add(p))
    bores.append(cq.Solid.makeCylinder(ri, L + 5, center, d))

# Internal cavities
body = body.cut(cq.Workplane("XY").workplane(offset=-1).circle(R_bore).extrude(H + 1))
body = body.cut(cq.Workplane("XY").add(cq.Solid.makeSphere(R_bore, center)))
for bsolid in bores:
    body = body.cut(cq.Workplane("XY").add(bsolid))

# Spark plug hole
body = body.cut(cq.Workplane("XY").add(
    cq.Solid.makeCylinder(7.0, 80, cq.Vector(0, 0, H - 5), cq.Vector(0, 0, 1))))

# Four bolt holes at quadrant points, through full height
for (x, y) in [(70, 0), (-70, 0), (0, 70), (0, -70)]:
    body = body.cut(cq.Workplane("XY").add(
        cq.Solid.makeCylinder(4.5, H + 4, cq.Vector(x, y, -2), cq.Vector(0, 0, 1))))

result = body
