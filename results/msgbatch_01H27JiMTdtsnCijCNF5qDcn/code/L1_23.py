import cadquery as cq

big = cq.Workplane("XY").center(0, 0).circle(25.0).extrude(50.0)
small = cq.Workplane("XY").center(40.0, 0).circle(15.0).extrude(50.0)

try:
    result = big.union(small)
except Exception:
    result = cq.Workplane("XY").newObject([cq.Compound.makeCompound([big.val(), small.val()])])
