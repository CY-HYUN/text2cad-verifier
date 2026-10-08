import cadquery as cq

R_out = 30.0
R_in = 20.0
L = 100.0

# YZ workplane: local x -> global Y, local y -> global Z, normal -> +X
profile = (
    cq.Workplane("YZ")
    .moveTo(R_out, 0)
    .threePointArc((0, R_out), (-R_out, 0))
    .lineTo(-R_in, 0)
    .threePointArc((0, R_in), (R_in, 0))
    .close()
)

result = profile.extrude(L)
