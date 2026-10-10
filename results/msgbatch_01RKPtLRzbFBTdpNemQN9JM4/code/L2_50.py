import cadquery as cq

# Shaft along X axis
left = cq.Workplane("YZ").circle(20).extrude(30)
mid = cq.Workplane("YZ").workplane(offset=30).circle(15).extrude(40)
right = cq.Workplane("YZ").workplane(offset=70).circle(10).extrude(30)
shaft = left.union(mid).union(right)

# Keyway on top of middle section: 20 long, 6 wide, 3.5 deep (flat bottom)
key = (cq.Workplane("XY")
       .box(20, 6, 4.5, centered=(True, True, False))
       .translate((50, 0, 11.5)))
shaft = shaft.cut(key)

# Center holes at each end
hole_left = cq.Workplane("YZ").circle(2.5).extrude(10)
hole_right = cq.Workplane("YZ").workplane(offset=90).circle(2.5).extrude(10)
shaft = shaft.cut(hole_left).cut(hole_right)

result = shaft
