import cadquery as cq

R_out = 20.0
wall = 2.0
R_in = R_out - wall
L = 100.0

def cyl(r, length, axis):
    if axis == "X":
        return cq.Solid.makeCylinder(r, length, cq.Vector(-length / 2, 0, 0), cq.Vector(1, 0, 0))
    else:
        return cq.Solid.makeCylinder(r, length, cq.Vector(0, -length / 2, 0), cq.Vector(0, 1, 0))

outer = cq.Workplane("XY").add(cyl(R_out, L, "X")).union(cq.Workplane("XY").add(cyl(R_out, L, "Y")))

# Equivalent to shelling with 2 mm walls and removing the four end faces
inner = cq.Workplane("XY").add(cyl(R_in, L + 2, "X")).union(cq.Workplane("XY").add(cyl(R_in, L + 2, "Y")))

result = outer.cut(inner)
