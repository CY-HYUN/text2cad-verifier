import cadquery as cq

cube = cq.Workplane("XY").box(50, 50, 50)

# Front hole (from face y=-25 going +Y, depth 30)
front = (cq.Workplane("XZ", origin=(0, -25, 0))
         .circle(7.5).extrude(-30))  # XZ normal is -Y, so negative extrude goes +Y

# Top hole (from face z=25 going down, depth 30)
top = (cq.Workplane("XY", origin=(0, 0, 25))
       .circle(7.5).extrude(-30))

result = cube.cut(front).cut(top)
