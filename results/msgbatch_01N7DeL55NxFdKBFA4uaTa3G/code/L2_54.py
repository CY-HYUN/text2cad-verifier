import cadquery as cq
import math

def pyramid(half, z0, apex_z):
    b = [cq.Vector(-half, -half, z0), cq.Vector(half, -half, z0),
         cq.Vector(half, half, z0), cq.Vector(-half, half, z0)]
    a = cq.Vector(0, 0, apex_z)
    faces = [cq.Face.makeFromWires(cq.Wire.makePolygon(b + [b[0]]))]
    for i in range(4):
        p, q = b[i], b[(i + 1) % 4]
        faces.append(cq.Face.makeFromWires(cq.Wire.makePolygon([p, q, a, p])))
    shell = cq.Shell.makeShell(faces)
    return cq.Workplane("XY").add(cq.Solid.makeSolid(shell))

# Outer solid pyramid: 40x40 base, apex at Z=40
outer = pyramid(20, 0, 40)

# Inner cavity: 30x30 base, apex at Z=30 (extended slightly below base for clean cut)
inner = pyramid(15.5, -1, 30)

result = outer.cut(inner)

# Triangular windows on each side face, leaving the edge framework
window = (
    cq.Workplane("YZ")
    .polyline([(-13, 4), (13, 4), (0, 30)])
    .close()
    .extrude(25)
)

for i in range(4):
    result = result.cut(window.rotate((0, 0, 0), (0, 0, 1), 90 * i))
