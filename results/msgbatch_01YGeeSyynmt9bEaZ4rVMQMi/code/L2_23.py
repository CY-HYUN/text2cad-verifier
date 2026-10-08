import cadquery as cq

# Datum plane heights
z1 = 0.0    # Plane 1 (bottom)
z2 = 20.0   # Plane 2 (top of square column)
z3 = 60.0   # Plane 3 (start of cylindrical column)
col_h = 20.0
wall = 2.0

side = 50.0
dia = 30.0

def body(s, d, ext=0.0):
    # Square column between Plane 1 and Plane 2
    sq = (cq.Workplane("XY").workplane(offset=z1 - ext)
          .rect(s, s).extrude(z2 - z1 + ext))
    # Loft transition between Plane 2 rectangle and Plane 3 circle
    lf = (cq.Workplane("XY").workplane(offset=z2)
          .rect(s, s).workplane(offset=z3 - z2)
          .circle(d / 2.0).loft(combine=True))
    # Cylindrical column on top of Plane 3
    cyl = (cq.Workplane("XY").workplane(offset=z3)
           .circle(d / 2.0).extrude(col_h + ext))
    return sq.union(lf).union(cyl)

outer = body(side, dia)
inner = body(side - 2 * wall, dia - 2 * wall, ext=1.0)

# Shell with top and bottom faces removed, 2 mm wall
result = outer.cut(inner)
