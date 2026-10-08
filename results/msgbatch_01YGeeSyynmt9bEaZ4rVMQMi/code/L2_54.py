import cadquery as cq
import math

def pyramid(half, z0, apex_z):
    b = [(-half, -half, z0), (half, -half, z0), (half, half, z0), (-half, half, z0)]
    a = (0, 0, apex_z)
    vecs = [cq.Vector(*p) for p in b]
    av = cq.Vector(*a)
    faces = [cq.Face.makeFromWires(cq.Wire.makePolygon(vecs, close=True))]
    for i in range(4):
        faces.append(cq.Face.makeFromWires(
            cq.Wire.makePolygon([vecs[i], vecs[(i + 1) % 4], av], close=True)))
    return cq.Solid.makeSolid(cq.Shell.makeShell(faces))

outer = pyramid(20, 0, 40)
# inner cavity: 30x30 at z=0 to apex z=30 (extended slightly below base for a clean cut)
inner = pyramid(15.5, -1, 30)

body = cq.Workplane("XY").add(outer).cut(cq.Workplane("XY").add(inner))

# triangular window cutter for the +X face, then rotated for all four faces
cutter = (cq.Workplane("YZ")
          .polyline([(-12, 3), (12, 3), (0, 27)]).close()
          .extrude(25))

for k in range(4):
    body = body.cut(cutter.rotate((0, 0, 0), (0, 0, 1), 90 * k))

result = body
