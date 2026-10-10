import cadquery as cq

# Base cube: 50 mm square extruded 25 mm each way along Z
cube = cq.Workplane("XY").rect(50, 50).extrude(25, both=True)

R = 30  # 60 mm diameter
off = 50  # circle centre offset so the arc cuts 5 mm into each side face

# Cylinders along Y (sketched on the front XZ plane), at x = ±off
cyl_y = (cq.Workplane("XZ").pushPoints([(off, 0), (-off, 0)])
         .circle(R).extrude(40, both=True))

# Cylinders along X (sketched on the right YZ plane), at y = ±off
cyl_x = (cq.Workplane("YZ").pushPoints([(off, 0), (-off, 0)])
         .circle(R).extrude(40, both=True))

result = cube.cut(cyl_y).cut(cyl_x)
