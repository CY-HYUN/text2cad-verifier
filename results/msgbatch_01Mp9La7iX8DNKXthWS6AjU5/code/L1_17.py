import cadquery as cq

block = cq.Workplane("XY").rect(60, 20, centered=False).extrude(30)

# Cylinder along Y axis, centered at x=30, z=0, radius 20, through the 20 mm thickness
cutter = (
    cq.Workplane("XZ", origin=(0, 0, 0))
    .center(30, 0)
    .circle(20)
    .extrude(-20)  # XZ normal is -Y, so negative extrude goes +Y
)

result = block.cut(cutter)
