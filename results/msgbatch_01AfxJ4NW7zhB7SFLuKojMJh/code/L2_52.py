import cadquery as cq

# Outer solid: side profile in the YZ plane, extruded across X (60 mm wide)
# 45-degree slope from front wall top (z=60) up to rear height (z=100)
pts = [(-30, 0), (30, 0), (30, 100), (10, 100), (-30, 60)]
outer = cq.Workplane("YZ").polyline(pts).close().extrude(30, both=True)

# Hollow interior, 5 mm walls, through top to bottom
inner = cq.Workplane("XY").box(50, 50, 120, centered=(True, True, False)).translate((0, 0, -10))
shell = outer.cut(inner)

# 20 mm hole through the tall rear wall (y = +30)
hole = (cq.Workplane("XZ").workplane(offset=-40)
        .center(0, 50).circle(10).extrude(20))
# XZ normal is -Y; offset -40 -> y=+40, extrude 20 toward -Y covers y=40..20
result = shell.cut(hole)
