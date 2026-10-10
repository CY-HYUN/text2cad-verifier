import cadquery as cq
import math

def pyramid(a, h, z0=0.0):
    b = [cq.Vector(-a, -a, z0), cq.Vector(a, -a, z0), cq.Vector(a, a, z0), cq.Vector(-a, a, z0)]
    ap = cq.Vector(0, 0, z0 + h)
    faces = []
    faces.append(cq.Face.makeFromWires(cq.Wire.makePolygon([b[0], b[3], b[2], b[1], b[0]])))
    for i in range(4):
        p, q = b[i], b[(i + 1) % 4]
        faces.append(cq.Face.makeFromWires(cq.Wire.makePolygon([p, q, ap, p])))
    sh = cq.Shell.makeShell(faces)
    return cq.Solid.makeSolid(sh)

outer = cq.Workplane("XY").add(pyramid(20, 40, 0))
# cavity from base upward (extend slightly below base to open it)
cav = cq.Workplane("XY").add(pyramid(16, 32, 0))
cav_ext = cq.Workplane("XY").box(32, 32, 2, centered=(True, True, False)).translate((0, 0, -2))
body = outer.cut(cav).cut(cav_ext)

tri = [(-12, 4), (12, 4), (0, 28)]
cut_x = cq.Workplane("YZ").polyline(tri).close().extrude(30, both=True)
cut_y = cq.Workplane("XZ").polyline(tri).close().extrude(30, both=True)

result = body.cut(cut_x).cut(cut_y)
