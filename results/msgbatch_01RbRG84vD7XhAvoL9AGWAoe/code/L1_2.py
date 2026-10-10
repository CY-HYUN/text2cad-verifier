import cadquery as cq

L = 120.0
OD = 40.0
ID = 25.0

result = (
    cq.Workplane("YZ")
    .circle(OD / 2)
    .circle(ID / 2)
    .extrude(L)
    .translate((-L / 2, 0, 0))
)
