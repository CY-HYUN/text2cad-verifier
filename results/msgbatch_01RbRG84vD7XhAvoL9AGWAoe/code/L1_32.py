import cadquery as cq

L, W, H = 80.0, 50.0, 30.0
c = 10.0

body = cq.Workplane("XY").box(L, W, H)

def tetra(corner, dirs):
    p0 = cq.Vector(*corner)
    p1 = p0 + cq.Vector(dirs[0] * c, 0, 0)
    p2 = p0 + cq.Vector(0, dirs[1] * c, 0)
    p3 = p0 + cq.Vector(0, 0, dirs[2] * c)
    tris = [(p0, p1, p2), (p0, p1, p3), (p0, p2, p3), (p1, p2, p3)]
    faces = [cq.Face.makeFromWires(cq.Wire.makePolygon(list(t), close=True)) for t in tris]
    return cq.Solid.makeSolid(cq.Shell.makeShell(faces))

# left-front-upper corner
t1 = tetra((-L / 2, -W / 2, H / 2), (1, 1, -1))
# right-rear-lower corner
t2 = tetra((L / 2, W / 2, -H / 2), (-1, -1, 1))

result = body.cut(cq.Workplane().add(t1)).cut(cq.Workplane().add(t2))
