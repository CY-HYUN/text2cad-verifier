import cadquery as cq
import math

# ---------------- Parameters ----------------
outer_d = 120.0
inner_d = 80.0          # bore (assumed)
height = 100.0
fin_d = 160.0
fin_t = 2.0
n_fins = 15
dome_r = 60.0
plug_d = 14.0
bolt_d = 8.0
bolt_r = (outer_d / 2 + inner_d / 2) / 2   # in the wall
total_h = height + dome_r

# ---------------- Sleeve ----------------
sleeve = (cq.Workplane("XY")
          .circle(outer_d / 2).circle(inner_d / 2)
          .extrude(height))

# ---------------- Fins (linear array along Z) ----------------
z0 = 3.0
pitch = (height - 2 * z0 - fin_t) / (n_fins - 1)
for i in range(n_fins):
    z = z0 + i * pitch
    fin = (cq.Workplane("XY").workplane(offset=z)
           .circle(fin_d / 2).circle(outer_d / 2 - 0.5)
           .extrude(fin_t))
    sleeve = sleeve.union(fin)

# ---------------- Hemispherical cover ----------------
sphere = cq.Workplane("XY").sphere(dome_r).translate((0, 0, height))
cutbox = cq.Workplane("XY").box(200, 200, 100).translate((0, 0, height - 50))
dome = sphere.cut(cutbox)
body = sleeve.union(dome)

# ---------------- Intake / exhaust tubes (inclined, asymmetric) ----------------
def tube(az_deg, el_deg, od, idd, r_start, r_end):
    az, el = math.radians(az_deg), math.radians(el_deg)
    d = cq.Vector(math.cos(el) * math.cos(az), math.cos(el) * math.sin(az), math.sin(el))
    p = cq.Vector(0, 0, height) + d * r_start
    L = r_end - r_start
    outer = cq.Solid.makeCylinder(od / 2, L, p, d)
    inner = cq.Solid.makeCylinder(idd / 2, L + 40, cq.Vector(0, 0, height) + d * (r_start - 20), d)
    return cq.Workplane("XY").add(outer), cq.Workplane("XY").add(inner)

t1o, t1i = tube(20, 40, 26, 18, 40, 90)     # intake
t2o, t2i = tube(200, 30, 22, 15, 40, 85)    # exhaust (asymmetric)
body = body.union(t1o).union(t2o).cut(t1i).cut(t2i)

# ---------------- Spark plug hole ----------------
plug = cq.Workplane("XY").add(
    cq.Solid.makeCylinder(plug_d / 2, dome_r + 2, cq.Vector(0, 0, height - 1), cq.Vector(0, 0, 1)))
body = body.cut(plug)

# ---------------- Bolt holes at four quadrant points ----------------
bolts = (cq.Workplane("XY").workplane(offset=-1)
         .pushPoints([(bolt_r, 0), (0, bolt_r), (-bolt_r, 0), (0, -bolt_r)])
         .circle(bolt_d / 2).extrude(total_h + 2))
body = body.cut(bolts)

result = body
