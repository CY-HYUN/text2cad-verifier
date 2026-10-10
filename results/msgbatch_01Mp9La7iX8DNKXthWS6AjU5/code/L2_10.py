import cadquery as cq

# U-shaped profile on the front plane (XZ), extruded 40 mm along +Y
pts = [(-40, 0), (40, 0), (40, 40), (30, 40), (30, 10), (-30, 10), (-30, 40), (-40, 40)]
body = cq.Workplane("XZ").polyline(pts).close().extrude(-40)

# Left flange: 10 mm through hole along X
left_hole = (cq.Workplane("YZ").workplane(offset=-41)
             .center(20, 20).circle(5).extrude(12))

# Right flange: 10 mm through hole
right_hole = (cq.Workplane("YZ").workplane(offset=29)
              .center(20, 20).circle(5).extrude(12))

# Right flange: 20 mm counterbore, 2 mm deep from the outer face (x=40)
right_cbore = (cq.Workplane("YZ").workplane(offset=38)
               .center(20, 20).circle(10).extrude(3))

result = body.cut(left_hole).cut(right_hole).cut(right_cbore)
