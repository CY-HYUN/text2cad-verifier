import cadquery as cq

R = 20.0  # ring (centerline) radius
r = 4.0   # tube cross-section radius (R > 2r so the links clear each other)

# Entity 1: horizontal ring
# Circle in the front (XY) plane, offset R along X, revolved about the Y axis.
ring1 = (
    cq.Workplane("XY")
    .center(R, 0)
    .circle(r)
    .revolve(360, (-R, 0, 0), (-R, 1, 0))  # axis through the global origin along Y
)

# Entity 2: vertical ring
# Same section, revolved about an axis parallel to X, with its centre raised by R
# so that it threads through the hole of ring 1 without touching it.
ring2 = cq.Workplane("XY").add(
    cq.Solid.makeTorus(R, r, pnt=cq.Vector(0, 0, R), dir=cq.Vector(1, 0, 0))
)

# Keep them as two independent bodies (multi-entity)
result = cq.Workplane("XY").add(
    cq.Compound.makeCompound([ring1.val(), ring2.val()])
)
