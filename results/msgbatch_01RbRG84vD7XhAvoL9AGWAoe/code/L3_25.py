import cadquery as cq
import math

H = 100.0
R_out = 60.0
R_bore = 40.0
fin_R = 80.0
fin_t = 2.0
n_fins = 15

# Cylinder liner
body = cq.Workplane("XY").circle(R_out).extrude(H)

# Cooling fins
pitch = H / n_fins
for i in range(n_fins):
    z = (i + 0.5) * pitch - fin_t / 2
    fin = (cq.Workplane("XY").workplane(offset=z)
           .circle(fin_R).circle(R_out - 1).extrude(fin_t))
    body = body.union(fin)

# Hemispherical combustion chamber cover
dome = cq.Workplane("XY").add(cq.Solid.makeSphere(R_out, cq.Vector(0, 0, H), angleDegrees1=0, angleDegrees2=90))
body = body.union(dome)

# Intake / exhaust pipes (asymmetric)
def pipe_dir(angle_from_vertical, side):
    a = math.radians(angle_from_vertical)
    return cq.Vector(side * math.sin(a), 0, math.cos(a))

pipes = [
    # (direction, outer radius, inner radius, length, y offset)
    (pipe_dir(50, 1), 13.0, 9.0, 90.0, 12.0),   # intake
    (pipe_dir(60, -1), 11.0, 7.5, 85.0, -10.0), # exhaust
]
start_c = cq.Vector(0, 0, H + 10)
for d, ro, ri, L, yo in pipes:
    p0 = start_c + cq.Vector(0, yo, 0)
    body = body.union(cq.Workplane("XY").add(cq.Solid.makeCylinder(ro, L, p0, d)))

# Internal cavities
bore = cq.Workplane("XY").workplane(offset=-1).circle(R_bore).extrude(H + 1)
body = body.cut(bore)
inner_dome = cq.Workplane("XY").add(cq.Solid.makeSphere(R_bore, cq.Vector(0, 0, H)))
body = body.cut(inner_dome)

for d, ro, ri, L, yo in pipes:
    p0 = start_c + cq.Vector(0, yo, 0)
    body = body.cut(cq.Workplane("XY").add(cq.Solid.makeCylinder(ri, L + 5, p0, d)))

# Spark plug hole (14 mm)
spark = cq.Workplane("XY").add(cq.Solid.makeCylinder(7.0, 40, cq.Vector(0, 0, H + 20), cq.Vector(0, 0, 1)))
body = body.cut(spark)

# Four bolt holes at quadrant points, through full liner height
bolt_r = 50.0
for k in range(4):
    a = math.radians(90 * k)
    x, y = bolt_r * math.cos(a), bolt_r * math.sin(a)
    hole = cq.Workplane("XY").add(cq.Solid.makeCylinder(4.5, H + 40, cq.Vector(x, y, -1), cq.Vector(0, 0, 1)))
    body = body.cut(hole)

result = body
