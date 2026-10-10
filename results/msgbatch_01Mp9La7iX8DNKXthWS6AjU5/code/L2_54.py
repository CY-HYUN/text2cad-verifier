import cadquery as cq
import math

def pyramid(h, H):
    a = cq.Vector(-h, -h, 0)
    b = cq.Vector(h, -h, 0)
    c = cq.Vector(h, h, 0)
    d = cq.Vector(-h, h, 0)
    ap = cq.Vector(0, 0, H)
    def face(pts):
        return cq.Face.makeFromWires(cq.Wire.makePolygon(pts + [pts[0]]))
    faces = [face([a, d, c, b]), face([a, b, ap]), face([b, c, ap]),
             face([c, d, ap]), face([d, a, ap])]
    return cq.Solid.makeSolid(cq.Shell.makeShell(faces))

outer = cq.Workplane("XY").add(pyramid(20, 40))
inner = cq.Workplane("XY").add(pyramid(15, 30))
hollow = outer.cut(inner)

# window cutter on the +Y face
s = math.sqrt(20**2 + 40**2)
k = 0.6
n = cq.Vector(0, 2, 1).normalized()
plane = cq.Plane(origin=(0, 40/3, 40/3), xDir=(1, 0, 0), normal=(n.x, n.y, n.z))
pts = [(-20*k, k*s/3), (20*k, k*s/3), (0, -k*2*s/3)]
cutter = (cq.Workplane(plane).polyline(pts).close().extrude(10, both=True))

result = hollow
for i in range(4):
    c = cutter.rotate((0, 0, 0), (0, 0, 1), 90 * i)
    result = result.cut(c)
