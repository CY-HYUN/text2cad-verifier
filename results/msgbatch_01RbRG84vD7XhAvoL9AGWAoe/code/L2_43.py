import cadquery as cq

outer = 60.0
inner = 40.0
height = 20.0
cyl_d = 40.0

# Square frame: 60x60 outer, 40x40 square hole
frame = (
    cq.Workplane("XY")
    .rect(outer, outer)
    .rect(inner, inner)
    .extrude(height)
)

# Cylinder centered in the hole, tangent to the four inner walls
cyl = cq.Workplane("XY").circle(cyl_d / 2.0).extrude(height)

try:
    result = frame.union(cyl, clean=False)
    if not result.val().isValid():
        raise ValueError
except Exception:
    result = cq.Workplane("XY").add(
        cq.Compound.makeCompound([frame.val(), cyl.val()])
    )
