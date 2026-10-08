import cadquery as cq

# Two externally tangent circles in the XY plane:
# large circle Ø50 (r=25) at the origin, small circle Ø30 (r=15) at x=40.
# Center distance 40 = 25 + 15, so the circles touch at x = 25.
big = cq.Workplane("XY").circle(25.0).extrude(50.0)
small = cq.Workplane("XY").center(40.0, 0).circle(15.0).extrude(50.0)

# Extrude both 50 mm along +Z and merge them into one solid
result = big.union(small)
