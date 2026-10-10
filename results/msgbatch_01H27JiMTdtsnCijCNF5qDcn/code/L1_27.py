import cadquery as cq

beam = cq.Workplane("XY").box(100, 20, 10, centered=(False, True, False))
base = cq.Workplane("XY").workplane(offset=-30).box(20, 20, 30, centered=(False, True, False))
result = beam.union(base)
