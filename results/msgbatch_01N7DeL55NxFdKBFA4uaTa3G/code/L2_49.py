import cadquery as cq

R = 20.0  # major radius
r = 4.0   # tube radius

# Entity 1: circle in front (XY) plane revolved about Y axis -> horizontal ring
ring1 = (
    cq.Workplane("XY")
    .center(R, 0)
    .circle(r)
    .revolve(360, (-R, 0, 0), (-R, 1, 0))
)

# Entity 2: same section in right (YZ) plane, revolved about an axis parallel to X
# Circle center at Y=R, Z=R; revolve axis along global X through (Y=0, Z=R)
# In YZ workplane local coords: local x -> global Y, local y -> global Z
ring2 = (
    cq.Workplane("YZ")
    .center(R, R)
    .circle(r)
    .revolve(360, (-R, -R + R, 0), (-R, -R + R, 1))
)

# Fallback-safe construction of ring2 via transform (ensures correct axis)
ring2 = (
    cq.Workplane("XY")
    .center(R, 0)
    .circle(r)
    .revolve(360, (-R, 0, 0), (-R, 1, 0))
    .rotate((0, 0, 0), (0, 0, 1), 90)   # axis Y -> axis X, ring now in YZ plane
    .translate((0, 0, R))               # passes through hole of ring1
)

result = cq.Workplane("XY").newObject(
    [cq.Compound.makeCompound([ring1.val(), ring2.val()])]
)
