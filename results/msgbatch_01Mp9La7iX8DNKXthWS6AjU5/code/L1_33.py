import cadquery as cq

outer = (cq.Workplane("YZ")
         .moveTo(-30, 0)
         .threePointArc((0, 30), (30, 0))
         .close()
         .extrude(100))
inner = (cq.Workplane("YZ")
         .moveTo(-20, 0)
         .threePointArc((0, 20), (20, 0))
         .close()
         .extrude(100))
result = outer.cut(inner)
