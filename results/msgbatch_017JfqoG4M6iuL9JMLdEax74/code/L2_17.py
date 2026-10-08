import cadquery as cq

L = 50.0

# Outer tube: OD 80, ID 70
outer = (
    cq.Workplane("XY")
    .circle(40)
    .circle(35)
    .extrude(L)
)

# Inner tube: OD 40, ID 30
inner = (
    cq.Workplane("XY")
    .circle(20)
    .circle(15)
    .extrude(L)
)

# Four radial ribs, 5 mm thick, bridging the gap between r=20 and r=35
# (each rib overlaps both tube walls slightly so the union fuses cleanly)
r_in = 19.0
r_out = 36.0
rib_len = r_out - r_in
rib_mid = (r_in + r_out) / 2.0
ribs = None
for ang in (0, 90, 180, 270):
    rib = (
        cq.Workplane("XY")
        .center(rib_mid, 0)
        .rect(rib_len, 5.0)
        .extrude(L)
        .rotate((0, 0, 0), (0, 0, 1), ang)
    )
    ribs = rib if ribs is None else ribs.union(rib)

result = outer.union(inner).union(ribs)
