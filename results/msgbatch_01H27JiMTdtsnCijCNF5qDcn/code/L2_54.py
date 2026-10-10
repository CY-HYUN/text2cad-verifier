import cadquery as cq
import math

def pyramid(half, h):
    base = [(-half, -half, 0), (half, -half, 0), (half, half, 0), (-half, half, 0)]
    apex = (0, 0, h)
    def face(pts):
        pts = [cq.Vector(*p) for p in pts]
        w = cq.Wire.makePolygon(pts + [pts[0]])
        return cq.Face.makeFromWires(w)
    faces = [face(base)]
    for i in range(4):
        faces.append(face([base[i], base[(i + 1) % 4], apex]))
    sh = cq.Shell.makeShell(faces)
    return cq.Workplane("XY").add(cq.Solid.makeSolid(sh))

outer = pyramid(20, 40)
inner = pyramid(15, 30)
hollow = outer.cut(inner)

# triangular window cutter on the -Y face (extruded along -Y from y=0)
def window():
    return (cq.Workplane("XZ")
            .polyline([(-10, 5), (10, 5), (0, 25)]).close()
            .extrude(25))

body = hollow
for i in range(4):
    w = window().rotate((0, 0, 0), (0, 0, 1), 90 * i)
    body = body.cut(w)

result = body
