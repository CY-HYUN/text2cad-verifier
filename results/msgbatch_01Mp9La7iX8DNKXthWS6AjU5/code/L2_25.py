import cadquery as cq

# Three 50x50x5 plates meeting at the origin corner
p_xy = cq.Workplane("XY").box(50, 50, 5, centered=False)
p_xz = cq.Workplane("XY").box(50, 5, 50, centered=False)
p_yz = cq.Workplane("XY").box(5, 50, 50, centered=False)

body = p_xy.union(p_xz).union(p_yz)

# Triangular rib at the Z-axis inner corner (legs 20 mm, thickness 5 mm, centred along edge)
rib_z = (cq.Workplane("XY")
         .polyline([(5, 5), (25, 5), (5, 25)]).close()
         .extrude(5)
         .translate((0, 0, 22.5)))

# Rotate about (1,1,1) by 120 degrees to get ribs on the X and Y edges
rib_x = rib_z.rotate((0, 0, 0), (1, 1, 1), 120)
rib_y = rib_z.rotate((0, 0, 0), (1, 1, 1), 240)

body = body.union(rib_z).union(rib_x).union(rib_y)

# 15 mm holes at the centre of each plate
hole_z = cq.Workplane("XY").center(25, 25).circle(7.5).extrude(5)
hole_y = (cq.Workplane("XZ").center(25, 25).circle(7.5).extrude(-5))
hole_x = (cq.Workplane("YZ").center(25, 25).circle(7.5).extrude(5))

result = body.cut(hole_z).cut(hole_y).cut(hole_x)
