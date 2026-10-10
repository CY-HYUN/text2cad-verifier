import cadquery as cq

length = 120.0
width = 40.0
thickness = 10.0
hole_d = 10.0
hole_offset = 20.0  # from each end

result = (
    cq.Workplane("XY")
    .box(length, width, thickness)
    .faces(">Z")
    .workplane()
    .pushPoints([(-(length / 2 - hole_offset), 0), (length / 2 - hole_offset, 0)])
    .hole(hole_d)
)
