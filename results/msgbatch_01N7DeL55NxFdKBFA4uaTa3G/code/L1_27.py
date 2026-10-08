import cadquery as cq

# Cantilever beam: 100 (X) x 20 (Y) x 10 (Z), sitting on the XY plane
beam = (
    cq.Workplane("XY")
    .center(50.0, 0.0)
    .rect(100.0, 20.0)
    .extrude(10.0)
)

# Base block: 20 x 20 footprint, 30 tall, under the left end of the beam
# Top face aligned with the beam's bottom face (z = 0), centered in width
base = (
    cq.Workplane("XY", origin=(0, 0, -30.0))
    .center(10.0, 0.0)
    .rect(20.0, 20.0)
    .extrude(30.0)
)

result = beam.union(base)
