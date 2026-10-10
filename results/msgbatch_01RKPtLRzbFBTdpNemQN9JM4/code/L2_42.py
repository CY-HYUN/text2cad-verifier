import cadquery as cq

# horizontal plate
h = cq.Workplane("XY").box(100, 60, 10, centered=(False, True, False))
# vertical plate
v = cq.Workplane("XY").box(10, 60, 100, centered=(False, True, False))

body = h.union(v)

# triangular rib, 10 thick centered on y=0
rib = (cq.Workplane("XZ")
       .polyline([(10, 10), (60, 10), (10, 60)]).close()
       .extrude(5, both=True))
body = body.union(rib)

# hole through horizontal plate (along Z)
hole_h = cq.Workplane("XY").center(55, 0).circle(10).extrude(10)
# hole through vertical plate (along X)
hole_v = (cq.Workplane("YZ").center(0, 55).circle(10).extrude(10))

result = body.cut(hole_h).cut(hole_v)
