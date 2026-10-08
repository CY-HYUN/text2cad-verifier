import cadquery as cq

L = 100.0
R = 20.0
t = 2.0
Ri = R - t

def cyl(r, length, direction):
    return cq.Workplane("XY").add(
        cq.Solid.makeCylinder(
            r, length,
            cq.Vector(*[-length / 2 * d for d in direction]),
            cq.Vector(*direction),
        )
    )

outer = cyl(R, L, (1, 0, 0)).union(cyl(R, L, (0, 1, 0)))
inner = cyl(Ri, L + 2, (1, 0, 0)).union(cyl(Ri, L + 2, (0, 1, 0)))

result = outer.cut(inner)
