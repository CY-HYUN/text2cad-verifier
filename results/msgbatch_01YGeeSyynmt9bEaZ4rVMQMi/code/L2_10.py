import cadquery as cq

# U-shaped profile on front (XZ) plane, extruded 40 mm along Y
pts = [(-40, 0), (40, 0), (40, 40), (30, 40), (30, 10),
       (-30, 10), (-30, 40), (-40, 40)]
body = cq.Workplane("XZ").polyline(pts).close().extrude(-40)  # extrude toward +Y

hole_y = 20.0   # middle of extrusion depth
hole_z = 25.0   # middle of flange above base

# Left flange: 10 mm through hole along X
left_hole = (cq.Workplane("YZ").workplane(offset=-41)
             .center(hole_y, hole_z).circle(5).extrude(12))
body = body.cut(left_hole)

# Right flange: 10 mm through hole
right_hole = (cq.Workplane("YZ").workplane(offset=29)
              .center(hole_y, hole_z).circle(5).extrude(12))
body = body.cut(right_hole)

# Right flange: 20 mm counterbore, 2 mm deep from outer face (x=40)
cbore = (cq.Workplane("YZ").workplane(offset=38)
         .center(hole_y, hole_z).circle(10).extrude(3))
body = body.cut(cbore)

result = body
