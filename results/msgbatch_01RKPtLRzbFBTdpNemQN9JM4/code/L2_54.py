import cadquery as cq
import math

def pyramid(a, h):
    A = cq.Vector(-a, -a, 0)
    B = cq.Vector(a, -a, 0)
    C = cq.Vector(a, a, 0)
    D = cq.Vector(-a, a, 0)
    P = cq.Vector(0, 0, h)
    def face(pts):
        return cq.Face.makeFromWires(cq.Wire.makePolygon(pts + [pts[0]]))
    faces = [face([A, D, C, B]),
             face([A, B, P]), face([B, C, P]),
             face([C, D, P]), face([D, A, P])]
    return cq.Solid.makeSolid(cq.Shell.makeShell(faces))

outer = cq.Workplane("XY").add(pyramid(20, 40))
cavity = cq.Workplane("XY").add(pyramid(16, 32))
body = outer.cut(cavity)

# triangular through-holes on each of the four sides
hole = (cq.Workplane("YZ")
        .polyline([(-13.5, 5), (13.5, 5), (0, 30)]).close()
        .extrude(25))
for k in range(4):
    h = hole.rotate((0, 0, 0), (0, 0, 1), 90 * k)
    body = body.cut(h)

result = body
