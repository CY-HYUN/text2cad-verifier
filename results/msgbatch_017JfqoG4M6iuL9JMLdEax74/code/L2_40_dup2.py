import cadquery as cq
import math

# Knurled anti-slip handle: D=30, L=60, crossed 45 deg V-grooves, depth 1, spacing ~2
R_out = 15.0
depth = 1.0
R_in = R_out - depth
L = 60.0

N_grooves = 47                  # grooves per direction around circumference (~2mm spacing)
cols = 2 * N_grooves            # angular grid columns
rows = 60                       # axial grid rows (h = 1.0 mm)
hz = L / rows

def pt(i, j):
    i = i % cols
    a = 2 * math.pi * i / cols
    r = R_in if (i + j) % 2 == 0 else R_out   # checkerboard: groove crossings / pyramid peaks
    return cq.Vector(r * math.cos(a), r * math.sin(a), j * hz)

P = [[pt(i, j) for j in range(rows + 1)] for i in range(cols)]

def tri(a, b, c):
    return cq.Face.makeFromWires(cq.Wire.makePolygon([a, b, c], close=True))

faces = []
for i in range(cols):
    i1 = (i + 1) % cols
    for j in range(rows):
        p00 = P[i][j]
        p10 = P[i1][j]
        p11 = P[i1][j + 1]
        p01 = P[i][j + 1]
        if (i + j) % 2 == 0:
            faces.append(tri(p00, p10, p11))
            faces.append(tri(p00, p11, p01))
        else:
            faces.append(tri(p00, p10, p01))
            faces.append(tri(p10, p11, p01))

# end caps (zig-zag planar polygons)
bottom = [P[i][0] for i in range(cols)]
top = [P[i][rows] for i in range(cols)]
faces.append(cq.Face.makeFromWires(cq.Wire.makePolygon(list(reversed(bottom)), close=True)))
faces.append(cq.Face.makeFromWires(cq.Wire.makePolygon(top, close=True)))

shell = cq.Shell.makeShell(faces)
solid = cq.Solid.makeSolid(shell)
solid = solid.fix()
if solid.Volume() < 0:
    solid = cq.Solid(solid.wrapped.Reversed())

result = cq.Workplane("XY").add(solid)
