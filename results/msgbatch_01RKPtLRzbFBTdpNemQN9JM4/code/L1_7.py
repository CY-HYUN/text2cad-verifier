import cadquery as cq

beam_x = cq.Workplane("XY").box(100, 20, 20)
beam_y = cq.Workplane("XY").box(20, 100, 20)
result = beam_x.union(beam_y)
