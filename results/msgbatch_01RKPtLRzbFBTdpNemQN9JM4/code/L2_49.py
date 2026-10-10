import cadquery as cq

t = 5.0  # ring thickness

# Ring A: horizontal flat ring (OD 40, ID 30), centered at origin
ring_a = (
    cq.Workplane("XY")
    .circle(20).circle(15)
    .extrude(t / 2, both=True)
)

# Ring B: vertical ring (same size), offset along X so it threads through A's hole
ring_b = (
    cq.Workplane("XZ")
    .center(-8, 0)
    .circle(20).circle(15)
    .extrude(t / 2, both=True)
)

# Two separate, interlocked solids in one compound (no contact)
result = cq.Workplane("XY").newObject([
    cq.Compound.makeCompound([ring_a.val(), ring_b.val()])
])
