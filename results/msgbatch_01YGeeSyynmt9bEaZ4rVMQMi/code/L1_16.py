import cadquery as cq

length = 120.0
width = 40.0
thickness = 10.0
hole_d = 10.0
edge_offset = 20.0

result = (
    cq.Workplane("XY")
    .rect(length, width)
    .extrude(thickness)
    .faces(">Z")
    .workplane()
    .pushPoints([(-length / 2 + edge_offset, 0), (length / 2 - edge_offset, 0)])
    .hole(hole_d)
)
