import cadquery as cq

cube = cq.Workplane("XY").box(60, 60, 60)

# Hole along X at Z=5 (circle drawn on the YZ plane)
h1 = (cq.Workplane("YZ").center(0, 5).circle(10).extrude(50, both=True))

# Hole along Y at Z=-5 (circle drawn on the XZ plane, X=0, Z=-5)
h2 = (cq.Workplane("XZ").center(0, -5).circle(10).extrude(50, both=True))

result = cube.cut(h1).cut(h2)
