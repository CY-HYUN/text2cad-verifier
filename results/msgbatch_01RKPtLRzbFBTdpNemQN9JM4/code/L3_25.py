import cadquery as cq
import math

# Cylinder liner: OD 120, height 100, bore 80
H = 100.0
R_out = 60.0
R_bore = 40.0
body = cq.Workplane("XY").circle(R_out).extrude(H)

# 15 fins, 2 mm thick, OD 160, evenly spaced along Z
n = 15
t = 2.0
pitch = (H - t) / (n - 1)
for i in range(n):
    z = i * pitch
    fin = cq.Workplane("XY").workplane(offset=z).circle(80).circle(R_out - 1).extrude(t)
    body = body.union(fin)

# Hemispherical combustion chamber cover on top
dome = cq.Workplane("XY").sphere(R_out).translate((0, 0, H))
dome = dome.intersect(cq.Workplane("XY").box(200, 200, 100, centered=(True, True, False)).translate((0, 0, H)))
body = body.union(dome)

# Intake and exhaust short pipes, asymmetric, oblique outward
def pipe(angle_deg, tilt_deg, length, ro, ri, zbase):
    p = (cq.Workplane("XY").circle(ro).extrude(length))
    p = p.rotate((0, 0, 0), (0, 1, 0), tilt_deg)
    p = p.translate((0, 0, 0))
    p = p.rotate((0, 0, 0), (0, 0, 1), angle_deg)
    return p.translate((0, 0, zbase))

def pipe_pair(angle, tilt, length, ro, ri, zbase):
    outer = pipe(angle, tilt, length, ro, ri, zbase)
    inner = pipe(angle, tilt, length + 2, ri, 0, zbase)
    return outer, inner

o1, i1 = pipe_pair(0, 55, 85, 11, 7, H + 15)       # intake
o2, i2 = pipe_pair(180, 40, 75, 9, 6, H + 20)      # exhaust
body = body.union(o1).union(o2)

# Bore through liner (below the dome)
bore = cq.Workplane("XY").circle(R_bore).extrude(H)
body = body.cut(bore)

# Port passages cut into the dome cavity
cav = cq.Workplane("XY").sphere(R_bore).translate((0, 0, H))
body = body.cut(cav)
body = body.cut(i1).cut(i2)

# Spark plug hole 14 mm diameter at center of cover
plug = cq.Workplane("XY").workplane(offset=H).circle(7).extrude(R_out + 5)
body = body.cut(plug)

# Four bolt holes through entire height at quadrant points
for sx in (-1, 1):
    for sy in (-1, 1):
        x = sx * 50 * math.cos(math.radians(45)) * 1.0
        y = sy * 50 * math.sin(math.radians(45)) * 1.0
        h = cq.Workplane("XY").center(x, y).circle(4).extrude(H)
        body = body.cut(h)

result = body
