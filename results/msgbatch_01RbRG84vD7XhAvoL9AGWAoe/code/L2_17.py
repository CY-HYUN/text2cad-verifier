import cadquery as cq

L = 50.0

outer = cq.Workplane("XY").circle(40).circle(35).extrude(L)
inner = cq.Workplane("XY").circle(20).circle(15).extrude(L)

result = outer.union(inner)

# Four radial ribs spanning the gap between the tubes (r = 20 to r = 35),
# with a little overlap into each tube wall for a clean union.
r0, r1 = 19.0, 36.0
rib_len = r1 - r0
rib_mid = (r0 + r1) / 2.0
for ang in [0, 90, 180, 270]:
    rib = (
        cq.Workplane("XY")
        .center(rib_mid, 0)
        .rect(rib_len, 5.0)
        .extrude(L)
        .rotate((0, 0, 0), (0, 0, 1), ang)
    )
    result = result.union(rib)
