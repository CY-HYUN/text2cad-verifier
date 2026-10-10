import cadquery as cq

cube = cq.Workplane("XY").box(50, 50, 50)
result = cube.faces(">Z").workplane().hole(20)
