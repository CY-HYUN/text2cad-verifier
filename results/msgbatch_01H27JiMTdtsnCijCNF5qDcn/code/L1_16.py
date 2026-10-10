import cadquery as cq

plate = cq.Workplane("XY").rect(120.0, 40.0).extrude(10.0)
result = (
    plate.faces(">Z").workplane(centerOption="CenterOfBoundBox")
    .pushPoints([(-40.0, 0), (40.0, 0)])
    .hole(10.0)
)
