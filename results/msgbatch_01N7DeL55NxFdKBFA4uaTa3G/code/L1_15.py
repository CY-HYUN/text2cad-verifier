import cadquery as cq

L = 50.0
d = 15.0

# Cube: 50x50 square centered on origin in XY, extruded 50 mm up Z
cube = cq.Workplane("XY").rect(L, L).extrude(L)

# Corner vertex chosen: (25, 25, 50)
V = cq.Vector(L/2, L/2, L)
A = cq.Vector(L/2 - d, L/2, L)
B = cq.Vector(L/2, L/2 - d, L)
C = cq.Vector(L/2, L/2, L - d)

def face(pts):
    return cq.Face.makeFromWires(cq.Wire.makePolygon(pts, close=True))

faces = [
    face([A, B, C]),
    face([V, B, A]),
    face([V, C, B]),
    face([V, A, C]),
]
tetra = cq.Solid.makeSolid(cq.Shell.makeShell(faces)).fix()

result = cube.cut(cq.Workplane("XY").add(tetra))
