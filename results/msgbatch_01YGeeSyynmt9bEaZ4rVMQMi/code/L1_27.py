import cadquery as cq

# Cantilever beam: 100 (X) x 20 (Y) x 10 (Z), sitting on the XY plane from Z=0 to Z=10
beam = (
    cq.Workplane("XY")
    .center(50.0, 0.0)
    .rect(100.0, 20.0)
    .extrude(10.0)
)

# Base block: 20 x 20 x 30, under the left end of the beam.
# Its top face (Z=0) meets the beam's bottom face; it is centred in Y.
base = (
    cq.Workplane("XY")
    .workplane(offset=-30.0)
    .center(10.0, 0.0)
    .rect(20.0, 20.0)
    .extrude(30.0)
)

result = beam.union(base)
