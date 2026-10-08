import cadquery as cq

# Dimensions
outer = 60.0
inner = 40.0
frame_h = 20.0
cyl_d = 40.0
cyl_h = 20.0

# Square frame: 60 x 60 outer, 40 x 40 through hole
frame = (
    cq.Workplane("XY")
    .rect(outer, outer)
    .rect(inner, inner)
    .extrude(frame_h)
)

# Cylinder centered in the hole, tangent to the four inner walls
cyl = cq.Workplane("XY").circle(cyl_d / 2.0).extrude(cyl_h)

try:
    result = frame.union(cyl)
    if not result.val().isValid():
        raise ValueError
except Exception:
    result = cq.Workplane("XY").newObject(
        [cq.Compound.makeCompound([frame.val(), cyl.val()])]
    )
