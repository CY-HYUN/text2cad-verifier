import cadquery as cq

# Outer body: cylinder D40 x H60, base on the XY plane
body = cq.Workplane("XY").circle(20).extrude(60)

# Internal spherical cavity D30, centred in the cylinder
sphere = cq.Workplane("XY").sphere(15).translate((0, 0, 30))

# Neck hole D10 from the top face down into the sphere
neck = cq.Workplane("XY").workplane(offset=30).circle(5).extrude(31)

result = body.cut(sphere).cut(neck)
