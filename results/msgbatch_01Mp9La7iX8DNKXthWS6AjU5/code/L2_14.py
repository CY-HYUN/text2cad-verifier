import cadquery as cq

cube = cq.Workplane("XY").box(60, 60, 60)

# Cut along Z (top view)
cut_z = cq.Workplane("XY").rect(40, 40).extrude(100, both=True)
# Cut along Y (front view)
cut_y = cq.Workplane("XZ").rect(40, 40).extrude(100, both=True)
# Cut along X (right view)
cut_x = cq.Workplane("YZ").rect(40, 40).extrude(100, both=True)

result = cube.cut(cut_z).cut(cut_y).cut(cut_x)
