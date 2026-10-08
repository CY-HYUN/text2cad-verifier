import cadquery as cq

# U-shaped cross-section on the front (XZ) plane
pts = [(-40, 0), (40, 0), (40, 40), (30, 40), (30, 10),
       (-30, 10), (-30, 40), (-40, 40)]
body = cq.Workplane("XZ").polyline(pts).close().extrude(20, both=True)

zc = 25.0  # hole centre height on the flanges

# Left flange: 10mm through hole
left_hole = (cq.Workplane("YZ").workplane(offset=-41)
             .center(0, zc).circle(5).extrude(12))
body = body.cut(left_hole)

# Right flange: 10mm through hole
right_hole = (cq.Workplane("YZ").workplane(offset=29)
              .center(0, zc).circle(5).extrude(12))
body = body.cut(right_hole)

# Right flange: 20mm counterbore, 2mm deep from outer face
cbore = (cq.Workplane("YZ").workplane(offset=38)
         .center(0, zc).circle(10).extrude(3))
body = body.cut(cbore)

result = body
