import cadquery as cq

# Base rectangular prism 60 x 40 x 40
result = cq.Workplane("XY").rect(60, 40).extrude(40)

# Two vertical blind holes on top, dia 10, spaced 30 apart, 30 deep
result = (
    result.faces(">Z").workplane()
    .pushPoints([(-15, 0), (15, 0)])
    .hole(10, 30)
)

# Horizontal hole from the +X side face, dia 10, connecting both vertical holes
# Vertical holes bottom at z=10; place channel axis at z=15
side_cut = (
    cq.Workplane("YZ", origin=(30, 0, 0))
    .center(0, 15)
    .circle(5)
    .extrude(-50)  # from x=30 inward to x=-20, passes through both holes
)
result = result.cut(side_cut)
