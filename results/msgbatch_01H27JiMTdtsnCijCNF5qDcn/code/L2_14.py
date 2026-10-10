import cadquery as cq

cube = cq.Workplane("XY").box(60, 60, 60)

cut_z = cq.Workplane("XY").rect(40, 40).extrude(100, both=True)
cut_x = cq.Workplane("YZ").rect(40, 40).extrude(100, both=True)
cut_y = cq.Workplane("XZ").rect(40, 40).extrude(100, both=True)

result = cube.cut(cut_z).cut(cut_x).cut(cut_y)
