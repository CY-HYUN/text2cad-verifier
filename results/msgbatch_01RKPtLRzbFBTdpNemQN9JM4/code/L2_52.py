import cadquery as cq

# Outer 60x60x100 column (x,y centered, z from 0 to 100)
outer = cq.Workplane("XY").box(60, 60, 100, centered=(True, True, False))

# Wedge above the slanted plane: front (y=-30) at z=60, rear (y=+30) at z=100
wedge = (cq.Workplane("YZ")
         .polyline([(-30, 60), (30, 100), (30, 130), (-30, 130)]).close()
         .extrude(40, both=True))

outer = outer.cut(wedge)

# Inner cavity 50x50 (5 mm walls), through top to bottom, also trimmed by slope
inner = cq.Workplane("XY").workplane(offset=-1).rect(50, 50).extrude(130)
inner = inner.cut(wedge)

body = outer.cut(inner)

# 20 mm hole through the taller rear wall (y=+30) along Y
hole = (cq.Workplane("XZ", origin=(0, 35, 0))
        .center(0, 50).circle(10).extrude(15))  # XZ normal is -Y, extrudes from y=35 to y=20
result = body.cut(hole)
