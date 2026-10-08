import cadquery as cq

L, W, H = 80.0, 50.0, 30.0
c = 10.0

box = cq.Workplane("XY").rect(L, W).extrude(H)

def tetra(corner, dx, dy, dz):
    x, y, z = corner
    p0 = cq.Vector(x, y, z)
    p1 = cq.Vector(x + dx, y, z)
    p2 = cq.Vector(x, y + dy, z)
    p3 = cq.Vector(x, y, z + dz)
    tris = [(p0, p1, p2), (p0, p1, p3), (p0, p2, p3), (p1, p2, p3)]
    faces = [cq.Face.makeFromWires(cq.Wire.makePolygon([a, b, d], close=True)) for a, b, d in tris]
    return cq.Solid.makeSolid(cq.Shell.makeShell(faces))

# Upper left front corner: x=-L/2, y=-W/2, z=H
t1 = tetra((-L / 2, -W / 2, H), c, c, -c)
# Lower right rear corner: x=L/2, y=W/2, z=0
t2 = tetra((L / 2, W / 2, 0), -c, -c, c)

result = box.cut(cq.Workplane().add(t1)).cut(cq.Workplane().add(t2))
