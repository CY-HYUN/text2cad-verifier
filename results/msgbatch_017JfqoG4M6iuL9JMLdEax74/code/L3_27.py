import cadquery as cq
import math

# ---------------- core block (rounded cube) ----------------
cube = cq.Workplane("XY").box(60, 60, 60)
sph = cq.Workplane("XY").sphere(42)
body = cube.intersect(sph)

# ---------------- helper: rotate a +Z feature to other directions ----------------
def orient(wp, d):
    if d == "+Z":
        return wp
    if d == "-Z":
        return wp.rotate((0, 0, 0), (1, 0, 0), 180)
    if d == "+X":
        return wp.rotate((0, 0, 0), (0, 1, 0), 90)
    if d == "-X":
        return wp.rotate((0, 0, 0), (0, 1, 0), -90)
    if d == "+Y":
        return wp.rotate((0, 0, 0), (1, 0, 0), -90)
    if d == "-Y":
        return wp.rotate((0, 0, 0), (1, 0, 0), 90)

# ---------------- top / bottom ports (OD40, L30, square flange 60x60) ----------------
def main_port_solid():
    pipe = cq.Workplane("XY").workplane(offset=25).circle(20).extrude(35)  # z 25..60
    flange = cq.Workplane("XY").workplane(offset=52).rect(60, 60).extrude(8)
    s = pipe.union(flange)
    # triangular ribs at four diagonal corners
    for k in range(4):
        rib = (cq.Workplane("XZ")
               .polyline([(17, 29), (28, 29), (17, 46)]).close()
               .extrude(2, both=True)
               .rotate((0, 0, 0), (0, 0, 1), 45 + 90 * k))
        s = s.union(rib)
    return s

def main_port_cuts():
    c = cq.Workplane("XY").circle(14).extrude(65)
    for sx in (-1, 1):
        for sy in (-1, 1):
            h = (cq.Workplane("XY").workplane(offset=50)
                 .center(22 * sx, 22 * sy).circle(3).extrude(12))
            c = c.union(h)
    return c

# ---------------- side ports (OD30, L25, round flange D50) ----------------
def side_port_solid():
    pipe = cq.Workplane("XY").workplane(offset=25).circle(15).extrude(30)  # to 55
    flange = cq.Workplane("XY").workplane(offset=49).circle(25).extrude(6)
    return pipe.union(flange)

def side_port_cuts():
    c = cq.Workplane("XY").circle(10).extrude(60)
    for k in range(4):
        a = math.radians(45 + 90 * k)
        h = (cq.Workplane("XY").workplane(offset=47)
             .center(20 * math.cos(a), 20 * math.sin(a)).circle(2.75).extrude(10))
        c = c.union(h)
    return c

# ---------------- assemble ----------------
for d in ("+Z", "-Z"):
    body = body.union(orient(main_port_solid(), d))
for d in ("+X", "-X", "+Y", "-Y"):
    body = body.union(orient(side_port_solid(), d))

# internal cavity and channels
body = body.cut(cq.Workplane("XY").sphere(20))
for d in ("+Z", "-Z"):
    body = body.cut(orient(main_port_cuts(), d))
for d in ("+X", "-X", "+Y", "-Y"):
    body = body.cut(orient(side_port_cuts(), d))

result = body
