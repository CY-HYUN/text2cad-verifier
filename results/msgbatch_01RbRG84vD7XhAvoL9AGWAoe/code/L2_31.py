import cadquery as cq

outer = cq.Workplane("XY").sphere(25)
inner = cq.Workplane("XY").sphere(20)
shell = outer.cut(inner)

# 20x20 square prism along X-axis, through both sides
cutter = cq.Workplane("YZ").rect(20, 20).extrude(30, both=True)

result = shell.cut(cutter)
