import cadquery as cq

# Datum planes
z1 = 0.0    # Plane 1 (bottom)
z2 = 20.0   # Plane 2 (top of square column)
z3 = 50.0   # Plane 3 (start of cylindrical column)
t = 2.0     # wall thickness

# ---------- Outer solid ----------
# Square column (50x50, 20 mm) between Plane 1 and Plane 2
square_col = cq.Workplane("XY").workplane(offset=z1).rect(50, 50).extrude(z2 - z1)

# Loft transition: rectangle on Plane 2 -> circle d30 on Plane 3
transition = (
    cq.Workplane("XY").workplane(offset=z2).rect(50, 50)
    .workplane(offset=z3 - z2).circle(15)
    .loft(combine=True)
)

# Cylindrical column (d30, 20 mm) on top of Plane 3
cyl_col = cq.Workplane("XY").workplane(offset=z3).circle(15).extrude(20)

outer = square_col.union(transition).union(cyl_col)

# ---------- Inner (cavity) solid for 2 mm shell, open top & bottom ----------
inner_sq = (
    cq.Workplane("XY").workplane(offset=z1 - 1)
    .rect(50 - 2 * t, 50 - 2 * t).extrude(z2 - z1 + 1.01)
)
inner_tr = (
    cq.Workplane("XY").workplane(offset=z2).rect(50 - 2 * t, 50 - 2 * t)
    .workplane(offset=z3 - z2).circle(15 - t)
    .loft(combine=True)
)
inner_cyl = (
    cq.Workplane("XY").workplane(offset=z3 - 0.01)
    .circle(15 - t).extrude(20 + 1.01)
)

result = outer.cut(inner_sq).cut(inner_tr).cut(inner_cyl)
